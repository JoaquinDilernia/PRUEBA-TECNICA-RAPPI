from pathlib import Path

import pytest

from financial_report import service
from financial_report.api_client import ExchangeAPIError
from financial_report.models import ExchangeRatesSnapshot


def _snapshot(rates: dict[str, float]) -> ExchangeRatesSnapshot:
    return ExchangeRatesSnapshot(base="USD", rates=rates, source_updated_at=None)


LATAM_SAMPLE_RATES = {
    "ARS": 1000.0,
    "BRL": 5.0,
    "CLP": 900.0,
    "COP": 3400.0,
    "MXN": 17.0,
    "PEN": 3.4,
    "UYU": 40.0,
}


def test_run_report_live_success(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(service, "fetch_rates", lambda: _snapshot(LATAM_SAMPLE_RATES))
    history_path = tmp_path / "history.json"
    reports_dir = tmp_path / "reports"

    result = service.run_report(history_path=history_path, reports_dir=reports_dir)

    assert result.source == "live"
    assert len(result.rows) == 7
    assert Path(result.csv_path).exists()
    assert history_path.exists()


def test_run_report_falls_back_when_api_fails(tmp_path: Path, monkeypatch):
    history_path = tmp_path / "history.json"
    reports_dir = tmp_path / "reports"

    # Primera corrida exitosa para poblar el historial.
    monkeypatch.setattr(service, "fetch_rates", lambda: _snapshot(LATAM_SAMPLE_RATES))
    service.run_report(history_path=history_path, reports_dir=reports_dir)

    # Segunda corrida: la API falla, debe caer al fallback del historial.
    def _fail():
        raise ExchangeAPIError("simulated outage")

    monkeypatch.setattr(service, "fetch_rates", _fail)
    result = service.run_report(history_path=history_path, reports_dir=reports_dir)

    assert result.source == "fallback"
    assert len(result.rows) == 7


def test_run_report_raises_when_api_fails_and_no_history(tmp_path: Path, monkeypatch):
    history_path = tmp_path / "history.json"
    reports_dir = tmp_path / "reports"

    def _fail():
        raise ExchangeAPIError("simulated outage")

    monkeypatch.setattr(service, "fetch_rates", _fail)

    with pytest.raises(ExchangeAPIError):
        service.run_report(history_path=history_path, reports_dir=reports_dir)


def test_run_report_appends_multiple_entries(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(service, "fetch_rates", lambda: _snapshot(LATAM_SAMPLE_RATES))
    history_path = tmp_path / "history.json"
    reports_dir = tmp_path / "reports"

    service.run_report(history_path=history_path, reports_dir=reports_dir)
    service.run_report(history_path=history_path, reports_dir=reports_dir)

    from financial_report.history import load_history

    assert len(load_history(history_path)) == 2
