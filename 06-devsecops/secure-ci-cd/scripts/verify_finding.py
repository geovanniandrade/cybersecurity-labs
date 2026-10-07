"""Exige o achado esperado e impede tratar erro do scanner como demonstração válida."""
import json
from pathlib import Path

report = json.loads(Path("evidence/bandit-fixture.json").read_text())
if report.get("errors"):
    raise SystemExit("O scanner apresentou erros.")
findings = [item for item in report["results"] if item["test_id"] == "B307"]
if not findings:
    raise SystemExit("O achado B307 esperado não foi detectado.")
for item in findings:
    print(f"{item['test_id']} | severidade {item['issue_severity']} | "
          f"confiança {item['issue_confidence']} | {item['filename']}:{item['line_number']}")
