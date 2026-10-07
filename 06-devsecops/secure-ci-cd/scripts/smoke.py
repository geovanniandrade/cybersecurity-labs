"""Valida versão, cálculo e rejeição de entrada no container implantado."""
import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def get(path):
    with urlopen("http://127.0.0.1:8080" + path, timeout=3) as response:
        return json.load(response)


for attempt in range(30):
    try:
        health = get("/health")
        break
    except (URLError, TimeoutError):
        time.sleep(1)
else:
    raise SystemExit("Container não respondeu em 30 tentativas.")
if health.get("status") != "ok" or health.get("version") != os.environ["APP_VERSION"]:
    raise SystemExit("Health check ou versão divergente.")
if get("/api/calculate?expression=10%2B20").get("result") != 30:
    raise SystemExit("Cálculo incorreto.")
try:
    get("/api/calculate?expression=eval")
except HTTPError as exc:
    if exc.code != 400:
        raise
else:
    raise SystemExit("Entrada inválida foi aceita.")
print(json.dumps({"health": health, "sum": 30, "invalid_input": 400}, indent=2))
