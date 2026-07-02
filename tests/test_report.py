import csv
from pathlib import Path

from financial_report import report
from financial_report.models import CurrencyRow


def test_build_rows_filters_only_latam_currencies(monkeypatch):
    monkeypatch.setattr(report, "random_variation", lambda: 0.01)
    rates = {"ARS": 1000.0, "BRL": 5.0, "USD": 1.0, "EUR": 0.9}  # USD/EUR no son LATAM

    rows = report.build_rows(rates, "2026-07-02")

    codes = {row.moneda for row in rows}
    assert codes == {"ARS", "BRL"}


def test_build_rows_skips_missing_latam_currencies(monkeypatch):
    monkeypatch.setattr(report, "random_variation", lambda: 0.0)
    rates = {"ARS": 1000.0}  # solo una de las 7 LATAM presente

    rows = report.build_rows(rates, "2026-07-02")

    assert len(rows) == 1
    assert rows[0].moneda == "ARS"
    assert rows[0].valor == 1000.0


def test_build_rows_applies_variation(monkeypatch):
    monkeypatch.setattr(report, "random_variation", lambda: 0.1)
    rates = {"ARS": 1000.0}

    rows = report.build_rows(rates, "2026-07-02")

    assert rows[0].valor == 1100.0
    assert rows[0].variacion == 0.1


def test_write_csv_roundtrip(tmp_path: Path):
    rows = [
        CurrencyRow(moneda="ARS", valor=1000.5, variacion=0.01, fecha="2026-07-02"),
        CurrencyRow(moneda="BRL", valor=5.25, variacion=-0.02, fecha="2026-07-02"),
    ]
    destination = tmp_path / "reports" / "reporte.csv"

    written_path = report.write_csv(rows, destination)

    assert written_path == destination
    with destination.open(encoding="utf-8") as csv_file:
        reader = list(csv.DictReader(csv_file))

    assert reader[0]["moneda"] == "ARS"
    assert reader[0]["fecha"] == "2026-07-02"
    assert float(reader[1]["variacion"]) == -0.02
