"""Servidor WSGI educacional. Não é um servidor de produção."""
import json
import os
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from app.calculator import calculate

PAGE = Path(__file__).with_name("index.html").read_bytes()


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    status = "200 OK"
    kind = "application/json; charset=utf-8"
    if environ.get("REQUEST_METHOD") != "GET":
        status, data = "405 Method Not Allowed", {"error": "Método não permitido"}
    elif path == "/":
        kind, data = "text/html; charset=utf-8", PAGE
    elif path == "/health":
        data = {"status": "ok", "version": os.getenv("APP_VERSION", "local")}
    elif path == "/api/calculate":
        try:
            query = parse_qs(environ.get("QUERY_STRING", ""))
            data = {"result": calculate(query.get("expression", [""])[0])}
        except ValueError as exc:
            status, data = "400 Bad Request", {"error": str(exc)}
    else:
        status, data = "404 Not Found", {"error": "Rota não encontrada"}
    body = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode()
    start_response(status, [("Content-Type", kind), ("Content-Length", str(len(body))),
                            ("X-Content-Type-Options", "nosniff"),
                            ("X-Frame-Options", "DENY"), ("Cache-Control", "no-store")])
    return [body]


if __name__ == "__main__":
    with make_server(os.getenv("HOST", "127.0.0.1"), 8080, application) as server:
        server.serve_forever()
