"""Soma restrita a dois inteiros positivos, sem executar código recebido."""
import re


def calculate(expression):
    if not isinstance(expression, str) or len(expression) > 100:
        raise ValueError("Informe dois inteiros separados por +.")
    match = re.fullmatch(r"\s*(\d{1,9})\s*\+\s*(\d{1,9})\s*", expression, flags=re.ASCII)
    if not match:
        raise ValueError("Informe dois inteiros de até 9 dígitos separados por +.")
    return int(match.group(1)) + int(match.group(2))
