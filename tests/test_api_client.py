from datetime import datetime, timezone

import pytest
import requests

from financial_report import api_client


class FakeResponse:
    def __init__(self, json_data=None, status_code=200, raise_json_error=False):
        self._json_data = json_data
        self.status_code = status_code
        self._raise_json_error = raise_json_error

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        if self._raise_json_error:
            raise ValueError("invalid json")
        return self._json_data


class FakeSession:
    def __init__(self, response=None, exception=None):
        self._response = response
        self._exception = exception

    def get(self, url, timeout):
        if self._exception is not None:
            raise self._exception
        return self._response


def _patch_session(monkeypatch, session: FakeSession) -> None:
    monkeypatch.setattr(api_client, "_build_session", lambda: session)


def test_fetch_rates_success(monkeypatch):
    payload = {
        "result": "success",
        "base_code": "USD",
        "time_last_update_unix": 1782950551,
        "rates": {"ARS": 1487.77, "BRL": 5.17},
    }
    _patch_session(monkeypatch, FakeSession(response=FakeResponse(json_data=payload)))

    snapshot = api_client.fetch_rates()

    assert snapshot.base == "USD"
    assert snapshot.rates == {"ARS": 1487.77, "BRL": 5.17}
    assert snapshot.source_updated_at == datetime.fromtimestamp(1782950551, tz=timezone.utc)


def test_fetch_rates_network_error_raises(monkeypatch):
    _patch_session(monkeypatch, FakeSession(exception=requests.ConnectionError("boom")))

    with pytest.raises(api_client.ExchangeAPIError):
        api_client.fetch_rates()


def test_fetch_rates_http_error_raises(monkeypatch):
    _patch_session(monkeypatch, FakeSession(response=FakeResponse(status_code=503)))

    with pytest.raises(api_client.ExchangeAPIError):
        api_client.fetch_rates()


def test_fetch_rates_invalid_json_raises(monkeypatch):
    _patch_session(monkeypatch, FakeSession(response=FakeResponse(raise_json_error=True)))

    with pytest.raises(api_client.ExchangeAPIError):
        api_client.fetch_rates()


def test_fetch_rates_non_success_result_raises(monkeypatch):
    payload = {"result": "error", "error-type": "invalid-key"}
    _patch_session(monkeypatch, FakeSession(response=FakeResponse(json_data=payload)))

    with pytest.raises(api_client.ExchangeAPIError, match="invalid-key"):
        api_client.fetch_rates()


def test_fetch_rates_missing_rates_field_raises(monkeypatch):
    payload = {"result": "success", "base_code": "USD"}
    _patch_session(monkeypatch, FakeSession(response=FakeResponse(json_data=payload)))

    with pytest.raises(api_client.ExchangeAPIError):
        api_client.fetch_rates()


def test_fetch_rates_missing_timestamp_leaves_source_updated_at_none(monkeypatch):
    payload = {"result": "success", "base_code": "USD", "rates": {"ARS": 1000.0}}
    _patch_session(monkeypatch, FakeSession(response=FakeResponse(json_data=payload)))

    snapshot = api_client.fetch_rates()

    assert snapshot.source_updated_at is None
