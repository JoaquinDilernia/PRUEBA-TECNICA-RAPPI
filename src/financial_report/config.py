"""Configuración centralizada, sobreescribible por variables de entorno.

Mantener toda la configuración acá (en vez de esparcida como constantes en
cada módulo) permite cambiar de entorno (dev/CI/prod) o de proveedor de API
sin tocar código.
"""

from __future__ import annotations

import os
from pathlib import Path

EXCHANGE_RATE_API_URL = os.environ.get(
    "EXCHANGE_RATE_API_URL", "https://open.er-api.com/v6/latest/USD"
)
REQUEST_TIMEOUT_SECONDS = float(os.environ.get("EXCHANGE_API_TIMEOUT_SECONDS", "10"))
MAX_RETRIES = int(os.environ.get("EXCHANGE_API_MAX_RETRIES", "2"))
RETRY_BACKOFF_SECONDS = float(os.environ.get("EXCHANGE_API_BACKOFF_SECONDS", "0.5"))

DATA_DIR = Path(os.environ.get("FINANCIAL_REPORT_DATA_DIR", "data"))
HISTORY_PATH = DATA_DIR / "history.json"
REPORTS_DIR = DATA_DIR / "reports"
