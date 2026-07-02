"""Construcción de filas del reporte y escritura a CSV."""

from __future__ import annotations

import csv
from pathlib import Path

from financial_report.currencies import LATAM_CURRENCIES
from financial_report.models import CurrencyRow
from financial_report.simulator import apply_variation, random_variation

CSV_FIELDNAMES = ["moneda", "valor", "variacion", "fecha"]


def build_rows(rates: dict[str, float], fecha: str) -> list[CurrencyRow]:
    """Filtra las monedas LATAM presentes en `rates` y les aplica una variación simulada.

    Monedas LATAM ausentes en `rates` se omiten (no todas las fuentes garantizan
    tener las 7 siempre disponibles).
    """
    rows: list[CurrencyRow] = []
    for code in LATAM_CURRENCIES:
        if code not in rates:
            continue
        variation = random_variation()
        value = apply_variation(rates[code], variation)
        rows.append(CurrencyRow(moneda=code, valor=value, variacion=variation, fecha=fecha))
    return rows


def write_csv(rows: list[CurrencyRow], destination: Path) -> Path:
    """Escribe las filas del reporte a un CSV, creando el directorio si falta."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_dict())
    return destination
