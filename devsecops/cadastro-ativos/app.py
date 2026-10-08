"""Painel de ativos de TI — AP II DevSecOps."""
import math
import os
import re
import secrets
import sqlite3
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for

TYPES = ("Notebook", "Desktop", "Servidor", "Monitor", "Rede", "Outro")
STATUSES = ("Disponível", "Em uso", "Em manutenção")
STATUS_CLASSES = {"Disponível": "available", "Em uso": "in-use", "Em manutenção": "maintenance"}
COLORS = ("#168779", "#80baa8", "#bdcfb0", "#dfbb6f", "#7f91ba", "#c3cbd6")
LIMITS = {"name": 100, "owner": 100, "tag": 60, "model": 120,
          "serial": 100, "location": 100, "notes": 1000}
FIELDS = ("name", "asset_type", "owner", "status", "tag", "model", "serial", "location", "notes")


def parse_price(text):
    """Aceita 4500, 4500.50 ou 4.500,50, sem ponto flutuante."""
    text = text.strip()
    if not text:
        return None
    if len(text) > 25:
        raise ValueError("Valor muito grande.")
    if "," in text:
        if not re.fullmatch(r"(?:\d+|\d{1,3}(?:\.\d{3})+),\d{1,2}", text):
            raise ValueError("Valor inválido.")
        text = text.replace(".", "").replace(",", ".")
    if not re.fullmatch(r"\d+(?:\.\d{1,2})?", text):
        raise ValueError("Valor inválido.")
    whole, _, fraction = text.partition(".")
    cents = int(whole) * 100 + int(fraction.ljust(2, "0") or "0")
    if cents > 100_000_000_000:
        raise ValueError("Valor muito grande.")
    return cents


def migrate(database):
    """Adiciona colunas sem alterar IDs, datas ou dados da versão inicial."""
    with sqlite3.connect(database, timeout=15) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            asset_type TEXT NOT NULL, owner TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
        columns = {row[1] for row in connection.execute("PRAGMA table_info(assets)")}
        migrations = {
            "status": "ALTER TABLE assets ADD COLUMN status TEXT NOT NULL DEFAULT 'Disponível'",
            "tag": "ALTER TABLE assets ADD COLUMN tag TEXT NOT NULL DEFAULT ''",
            "model": "ALTER TABLE assets ADD COLUMN model TEXT NOT NULL DEFAULT ''",
            "serial": "ALTER TABLE assets ADD COLUMN serial TEXT NOT NULL DEFAULT ''",
            "location": "ALTER TABLE assets ADD COLUMN location TEXT NOT NULL DEFAULT ''",
            "notes": "ALTER TABLE assets ADD COLUMN notes TEXT NOT NULL DEFAULT ''",
            "price_cents": "ALTER TABLE assets ADD COLUMN price_cents INTEGER",
        }
        for name, statement in migrations.items():
            if name not in columns:
                connection.execute(statement)
        connection.execute("""CREATE UNIQUE INDEX IF NOT EXISTS unique_asset_tag
            ON assets(tag COLLATE NOCASE) WHERE tag <> ''""")


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("APP_SECRET") or secrets.token_hex(32),
        DATABASE=os.environ.get("DATABASE_PATH", "data/ativos.sqlite3"),
        MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config:
        app.config.update(test_config)
    database = Path(app.config["DATABASE"])
    database.parent.mkdir(parents=True, exist_ok=True)
    migrate(database)

    def read_assets():
        with sqlite3.connect(database, timeout=15) as connection:
            connection.row_factory = sqlite3.Row
            return connection.execute("SELECT * FROM assets ORDER BY id DESC").fetchall()

    def get_asset(asset_id):
        with sqlite3.connect(database, timeout=15) as connection:
            connection.row_factory = sqlite3.Row
            asset = connection.execute("SELECT * FROM assets WHERE id=?", (asset_id,)).fetchone()
        if asset is None:
            abort(404)
        return asset

    @app.before_request
    def csrf():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        if request.method == "POST" and not secrets.compare_digest(
                request.form.get("csrf_token", ""), session["csrf_token"]):
            abort(400, description="Formulário expirado. Recarregue a página antes de salvar.")

    @app.after_request
    def headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'self'")
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.context_processor
    def common():
        return dict(asset_types=TYPES, statuses=STATUSES, status_classes=STATUS_CLASSES)

    @app.template_filter("date_br")
    def date_br(value):
        return "/".join(reversed(value[:10].split("-"))) if value else "—"

    @app.template_filter("brl")
    def brl(cents):
        if cents is None:
            return "Não informado"
        return "R$ " + format(cents // 100, ",").replace(",", ".") + f",{cents % 100:02d}"

    def render_inventory(inventory=False):
        all_assets = read_assets()
        filters = {key: request.args.get(key, "").strip() for key in ("q", "type", "status")}
        if len(filters["q"]) > 200:
            abort(400, description="A busca deve ter até 200 caracteres.")
        if filters["type"] and filters["type"] not in TYPES:
            abort(400, description="Filtro de tipo inválido.")
        if filters["status"] and filters["status"] not in STATUSES:
            abort(400, description="Filtro de status inválido.")
        q = filters["q"].casefold()
        assets = [a for a in all_assets if
                  (not q or any(q in a[field].casefold() for field in
                   ("name", "owner", "tag", "location", "model", "serial"))) and
                  (not filters["type"] or a["asset_type"] == filters["type"]) and
                  (not filters["status"] or a["status"] == filters["status"])]
        total = len(all_assets)
        counts = {status: sum(a["status"] == status for a in all_assets) for status in STATUSES}
        distribution, offset = [], 0
        circumference = 2 * math.pi * 62
        for kind, color in zip(TYPES, COLORS):
            count = sum(a["asset_type"] == kind for a in all_assets)
            fraction = count / total if total else 0
            length = fraction * circumference
            distribution.append(dict(label=kind, count=count, color=color,
                                     percent=round(fraction * 100), length=length,
                                     offset=-offset, circumference=circumference))
            offset += length
        filtered = any(filters.values())
        priced = [a for a in all_assets if a["price_cents"] is not None]
        return render_template("index.html", inventory=inventory, total=total, counts=counts,
                               assets=assets if inventory or filtered else assets[:8],
                               result_count=len(assets), filters=filters, filtered=filtered,
                               distribution=distribution, investment=sum(a["price_cents"] for a in priced),
                               priced_count=len(priced), deleted=request.args.get("deleted") == "1")

    @app.get("/")
    def index():
        return render_inventory()

    @app.get("/ativos")
    def inventory():
        return render_inventory(True)

    def asset_form(asset=None):
        values = dict(asset) if asset else {**{field: "" for field in LIMITS},
                                           "asset_type": "", "status": "Disponível"}
        cents = asset["price_cents"] if asset else None
        values["price"] = f"{cents // 100},{cents % 100:02d}" if cents is not None else ""
        error = None
        if request.method == "POST":
            values = {field: request.form.get(field, "").strip() for field in (*FIELDS, "price")}
            if not values["name"] or not values["owner"]:
                error = "Informe o nome do ativo e a pessoa responsável."
            elif values["asset_type"] not in TYPES:
                error = "Selecione um tipo de ativo válido."
            elif values["status"] not in STATUSES:
                error = "Selecione um status válido."
            elif any(len(values[field]) > limit for field, limit in LIMITS.items()):
                error = "Um dos campos ultrapassou o limite de caracteres indicado."
            try:
                price = parse_price(values["price"])
            except ValueError:
                error = "Informe um valor entre 0 e 1 bilhão de reais, com até duas casas decimais. Ex.: 4.500,50."
            if not error:
                try:
                    with sqlite3.connect(database, timeout=15) as connection:
                        args = tuple(values[field] for field in FIELDS) + (price,)
                        if asset:
                            connection.execute("""UPDATE assets SET name=?, asset_type=?, owner=?,
                                status=?, tag=?, model=?, serial=?, location=?, notes=?, price_cents=?
                                WHERE id=?""", (*args, asset["id"]))
                            asset_id = asset["id"]
                        else:
                            cursor = connection.execute("""INSERT INTO assets
                                (name, asset_type, owner, status, tag, model, serial, location, notes, price_cents)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", args)
                            asset_id = cursor.lastrowid
                    return redirect(url_for("detail", asset_id=asset_id, saved="1"), code=303)
                except sqlite3.IntegrityError:
                    error = "Este patrimônio já está cadastrado. Use um código diferente."
        return render_template("form.html", values=values, asset=asset, error=error,
                               limits=LIMITS), 400 if error else 200

    @app.route("/ativos/novo", methods=["GET", "POST"])
    def new_asset():
        return asset_form()

    @app.get("/ativos/<int:asset_id>")
    def detail(asset_id):
        return render_template("detail.html", asset=get_asset(asset_id), saved=request.args.get("saved") == "1")

    @app.route("/ativos/<int:asset_id>/editar", methods=["GET", "POST"])
    def edit_asset(asset_id):
        return asset_form(get_asset(asset_id))

    @app.route("/ativos/<int:asset_id>/remover", methods=["GET", "POST"])
    def remove_asset(asset_id):
        asset = get_asset(asset_id)
        if request.method == "POST":
            if request.form.get("confirm") != "yes":
                abort(400, description="Confirme a remoção antes de continuar.")
            with sqlite3.connect(database, timeout=15) as connection:
                connection.execute("DELETE FROM assets WHERE id=?", (asset_id,))
            return redirect(url_for("inventory", deleted="1"), code=303)
        return render_template("remove.html", asset=asset)

    @app.get("/health")
    def health():
        with sqlite3.connect(database, timeout=15) as connection:
            connection.execute("SELECT 1 FROM assets LIMIT 1").fetchone()
        return {"status": "ok"}

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(413)
    def error_page(error):
        message = {404: "Não encontramos este ativo ou esta página.",
                   413: "O formulário enviado é muito grande."}.get(error.code, error.description)
        return render_template("error.html", code=error.code, message=message), error.code

    return app
