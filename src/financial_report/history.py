"""Historial de ejecuciones, persistido en un JSON local.

Cada entrada guarda las tasas base (pre-variación) usadas en esa corrida,
para poder usarlas como fallback si una corrida futura no puede alcanzar la API.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from financial_report.config import HISTORY_PATH as DEFAULT_HISTORY_PATH
from financial_report.models import ExchangeRatesSnapshot

__all__ = [
    "DEFAULT_HISTORY_PATH",
    "load_history",
    "append_run",
    "get_last_run",
    "get_last_snapshot",
]


def load_history(path: Path = DEFAULT_HISTORY_PATH) -> list[dict[str, Any]]:
    """Carga el historial completo. Devuelve lista vacía si el archivo no existe o está vacío."""
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []
    return json.loads(content)


def append_run(entry: dict[str, Any], path: Path = DEFAULT_HISTORY_PATH) -> None:
    """Agrega una corrida al historial y persiste el archivo."""
    history = load_history(path)
    history.append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")


def get_last_run(path: Path = DEFAULT_HISTORY_PATH) -> dict[str, Any] | None:
    """Última corrida guardada (independientemente de si fue 'live' o 'fallback'), o None."""
    history = load_history(path)
    return history[-1] if history else None


def get_last_snapshot(path: Path = DEFAULT_HISTORY_PATH) -> ExchangeRatesSnapshot | None:
    """Reconstruye el snapshot de tasas de la última corrida, para usar como fallback."""
    last_run = get_last_run(path)
    if last_run is None:
        return None

    source_updated_at_raw = last_run.get("source_updated_at")
    source_updated_at = (
        datetime.fromisoformat(source_updated_at_raw) if source_updated_at_raw else None
    )
    return ExchangeRatesSnapshot(
        base="USD",
        rates=last_run["rates"],
        source_updated_at=source_updated_at,
    )
