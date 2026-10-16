import re
import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app, parse_price


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = {"TESTING": True, "SECRET_KEY": "test-only", "DATABASE": str(Path(self.temp.name) / "assets.db")}
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def token(self, path="/ativos/novo"):
        html = self.client.get(path).get_data(as_text=True)
        return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)

    def register(self, **changes):
        data = {"csrf_token": self.token(), "name": "Notebook TI", "asset_type": "Notebook",
                "owner": "Ana Silva", "status": "Disponível"}
        data.update(changes)
        return self.client.post("/ativos/novo", data=data)

    def rows(self):
        with sqlite3.connect(self.config["DATABASE"]) as connection:
            connection.row_factory = sqlite3.Row
            return connection.execute("SELECT * FROM assets ORDER BY id").fetchall()

    def test_register_details_and_restart_preserves_data(self):
        response = self.register(tag="PAT-01", model="Dell Latitude", serial="LAB001",
                                 location="Sala de TI", price="4.500,50", notes="Uso de laboratório")
        self.assertEqual(response.status_code, 303)
        restarted = create_app(self.config).test_client()
        html = restarted.get(response.location).get_data(as_text=True)
        for text in ("PAT-01", "Dell Latitude", "LAB001", "Sala de TI", "R$ 4.500,50", "Uso de laboratório"):
            self.assertIn(text, html)
        self.assertEqual(self.rows()[0]["price_cents"], 450050)

    def test_migration_preserves_original_schema_records_and_ids(self):
        legacy = Path(self.temp.name) / "legacy.db"
        with sqlite3.connect(legacy) as connection:
            connection.execute("""CREATE TABLE assets(id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, asset_type TEXT NOT NULL, owner TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
            connection.execute("INSERT INTO assets VALUES (7, 'notebook 001', 'Notebook', 'Vinicius', '2026-10-07 23:26:00')")
        app = create_app({**self.config, "DATABASE": str(legacy)})
        create_app({**self.config, "DATABASE": str(legacy)})  # migração idempotente
        self.assertEqual(app.test_client().get("/ativos/7").status_code, 200)
        with sqlite3.connect(legacy) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute("SELECT * FROM assets").fetchone()
            self.assertEqual((row["id"], row["name"], row["owner"], row["created_at"]),
                             (7, "notebook 001", "Vinicius", "2026-10-07 23:26:00"))
            self.assertEqual(row["status"], "Disponível")
            self.assertEqual(row["location"], "")
            self.assertIsNone(row["price_cents"])

    def test_edit_keeps_id_date_and_updates_all_fields(self):
        self.register()
        original = self.rows()[0]
        response = self.client.post("/ativos/1/editar", data={"csrf_token": self.token("/ativos/1/editar"),
            "name": "Notebook atualizado", "asset_type": "Desktop", "owner": "Leonardo",
            "status": "Em manutenção", "tag": "PAT-99", "location": "Bancada", "price": "100,01"})
        self.assertEqual(response.status_code, 303)
        row = self.rows()[0]
        self.assertEqual((row["id"], row["created_at"]), (original["id"], original["created_at"]))
        self.assertEqual((row["owner"], row["status"], row["price_cents"]), ("Leonardo", "Em manutenção", 10001))

    def test_missing_invalid_and_oversized_fields_are_rejected(self):
        for changes in ({"name": " "}, {"owner": ""}, {"asset_type": "Invalid"},
                        {"status": "Invalid"}, {"name": "a"*101}, {"notes": "a"*1001},
                        {"price": "-1"}, {"price": "NaN"}, {"price": "4.500,555"}):
            with self.subTest(changes=changes):
                self.assertEqual(self.register(**changes).status_code, 400)
        self.assertEqual(len(self.rows()), 0)

    def test_optional_price_blank_zero_and_exact_cents(self):
        self.assertIsNone(parse_price(""))
        for text, expected in (("0", 0), ("0,10", 10), ("4500.50", 450050), ("4.500,50", 450050)):
            self.assertEqual(parse_price(text), expected)
        self.register()
        self.assertIsNone(self.rows()[0]["price_cents"])
        self.assertIn("Não informado", self.client.get("/ativos/1").get_data(as_text=True))

    def test_duplicate_patrimony_rejected_case_insensitively(self):
        self.assertEqual(self.register(tag="PAT-01").status_code, 303)
        self.assertEqual(self.register(tag="pat-01").status_code, 400)
        self.assertEqual(self.register(tag="").status_code, 303)
        self.assertEqual(self.register(tag="").status_code, 303)
        self.assertEqual(len(self.rows()), 3)

    def test_search_filters_and_global_dashboard_totals(self):
        self.register(name="NOTEBOOK-FIN", owner="João", location="São Paulo", status="Em uso", price="0,10")
        self.register(name="SERVIDOR-TI", asset_type="Servidor", status="Em manutenção", price="0,20")
        self.register(name="MONITOR-TI", asset_type="Monitor")
        page = self.client.get("/?q=JOÃO&type=Notebook&status=Em+uso").get_data(as_text=True)
        self.assertIn("NOTEBOOK-FIN", page)
        self.assertNotIn("SERVIDOR-TI", page)
        self.assertIn('id="metric-total">3<', page)
        self.assertIn('id="metric-in-use">1<', page)
        self.assertIn('id="metric-available">1<', page)
        self.assertIn('id="metric-maintenance">1<', page)
        self.assertIn("R$ 0,30", page)
        self.assertIn("Nenhum ativo encontrado", self.client.get("/ativos?q=xxxxx").get_data(as_text=True))
        self.assertEqual(self.client.get("/ativos?type=Inválido").status_code, 400)

    def test_remove_get_never_deletes_and_confirmation_is_required(self):
        self.register(name="Remover")
        self.register(name="Preservar")
        token = self.token("/ativos/1/remover")
        self.assertEqual(len(self.rows()), 2)
        self.assertEqual(self.client.post("/ativos/1/remover", data={"csrf_token": token}).status_code, 400)
        self.assertEqual(len(self.rows()), 2)
        result = self.client.post("/ativos/1/remover", data={"csrf_token": token, "confirm": "yes"})
        self.assertEqual(result.status_code, 303)
        self.assertEqual([r["name"] for r in self.rows()], ["Preservar"])
        self.assertEqual(self.client.get("/ativos/1").status_code, 404)

    def test_all_mutations_require_csrf(self):
        self.register()
        for path in ("/ativos/novo", "/ativos/1/editar", "/ativos/1/remover"):
            self.assertEqual(self.client.post(path, data={"confirm": "yes"}).status_code, 400)
        self.assertEqual(len(self.rows()), 1)

    def test_sql_text_and_html_are_handled_as_data(self):
        text = "Notebook'); DROP TABLE assets; --"
        self.assertEqual(self.register(name=text, notes="<script>alert(1)</script>").status_code, 303)
        self.assertEqual(self.rows()[0]["name"], text)
        page = self.client.get("/ativos/1").get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_health_headers_and_missing_asset(self):
        response = self.client.get("/health")
        self.assertEqual(response.json, {"status": "ok"})
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("frame-ancestors 'none'", response.headers["Content-Security-Policy"])
        self.assertEqual(self.client.get("/ativos/999/editar").status_code, 404)
        self.assertEqual(self.client.get("/ativos/999/remover").status_code, 404)


if __name__ == "__main__":
    unittest.main()
