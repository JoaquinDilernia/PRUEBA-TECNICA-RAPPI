from pathlib import Path

from financial_report import history


def test_load_history_missing_file_returns_empty(tmp_path: Path):
    path = tmp_path / "history.json"
    assert history.load_history(path) == []


def test_append_and_load_history(tmp_path: Path):
    path = tmp_path / "history.json"
    entry = {"timestamp": "2026-07-02T10:00:00", "source": "live", "rates": {"ARS": 1000.0}}

    history.append_run(entry, path)
    loaded = history.load_history(path)

    assert len(loaded) == 1
    assert loaded[0] == entry


def test_append_run_accumulates(tmp_path: Path):
    path = tmp_path / "history.json"
    history.append_run({"timestamp": "1", "rates": {}}, path)
    history.append_run({"timestamp": "2", "rates": {}}, path)

    assert len(history.load_history(path)) == 2


def test_get_last_run_returns_most_recent(tmp_path: Path):
    path = tmp_path / "history.json"
    history.append_run({"timestamp": "1", "rates": {}}, path)
    history.append_run({"timestamp": "2", "rates": {}}, path)

    assert history.get_last_run(path)["timestamp"] == "2"


def test_get_last_run_empty_history_returns_none(tmp_path: Path):
    path = tmp_path / "history.json"
    assert history.get_last_run(path) is None


def test_get_last_snapshot_reconstructs_rates(tmp_path: Path):
    path = tmp_path / "history.json"
    history.append_run(
        {
            "timestamp": "1",
            "source_updated_at": "2026-07-02T00:02:31+00:00",
            "rates": {"ARS": 1000.0, "BRL": 5.0},
        },
        path,
    )

    snapshot = history.get_last_snapshot(path)

    assert snapshot is not None
    assert snapshot.rates == {"ARS": 1000.0, "BRL": 5.0}
    assert snapshot.source_updated_at.isoformat() == "2026-07-02T00:02:31+00:00"


def test_get_last_snapshot_handles_missing_source_updated_at(tmp_path: Path):
    path = tmp_path / "history.json"
    history.append_run({"timestamp": "1", "rates": {"ARS": 1000.0}}, path)

    snapshot = history.get_last_snapshot(path)

    assert snapshot.source_updated_at is None


def test_get_last_snapshot_no_history_returns_none(tmp_path: Path):
    path = tmp_path / "history.json"
    assert history.get_last_snapshot(path) is None
