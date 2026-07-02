"""Análisis del conjunto de filas de un reporte."""

from __future__ import annotations

from financial_report.models import CurrencyRow


def most_devalued(rows: list[CurrencyRow]) -> CurrencyRow:
    """Moneda con la variación más negativa del día."""
    if not rows:
        raise ValueError("No hay filas para analizar")
    return min(rows, key=lambda row: row.variacion)


def most_stable(rows: list[CurrencyRow]) -> CurrencyRow:
    """Moneda con la variación más cercana a cero (en valor absoluto) del día."""
    if not rows:
        raise ValueError("No hay filas para analizar")
    return min(rows, key=lambda row: abs(row.variacion))
