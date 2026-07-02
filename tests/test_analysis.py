import pytest

from financial_report.analysis import most_devalued, most_stable
from financial_report.models import CurrencyRow


def _row(moneda: str, variacion: float) -> CurrencyRow:
    return CurrencyRow(moneda=moneda, valor=100.0, variacion=variacion, fecha="2026-07-02")


def test_most_devalued_is_most_negative():
    rows = [_row("ARS", 0.01), _row("BRL", -0.02), _row("CLP", 0.001)]
    assert most_devalued(rows).moneda == "BRL"


def test_most_stable_is_closest_to_zero():
    rows = [_row("ARS", 0.01), _row("BRL", -0.02), _row("CLP", 0.001)]
    assert most_stable(rows).moneda == "CLP"


def test_most_stable_considers_negative_close_to_zero():
    rows = [_row("ARS", 0.015), _row("BRL", -0.001), _row("CLP", 0.02)]
    assert most_stable(rows).moneda == "BRL"


def test_most_devalued_empty_raises():
    with pytest.raises(ValueError):
        most_devalued([])


def test_most_stable_empty_raises():
    with pytest.raises(ValueError):
        most_stable([])
