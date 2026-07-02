"""Historial de ejecuciones, persistido en un JSON local.

Cada entrada guarda las tasas base (pre-variación) usadas en esa corrida,
para poder usarlas como fallback si una corrida futura no puede alcanzar la API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_HISTORY_PATH = Path("data/history.json")


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


def get_last_rates(path: Path = DEFAULT_HISTORY_PATH) -> dict[str, float] | None:
    """Tasas base de la última corrida guardada, para usar como fallback."""
    last_run = get_last_run(path)
    return last_run["rates"] if last_run else None
