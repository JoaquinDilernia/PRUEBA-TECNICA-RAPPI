"""Cliente para la API de tipos de cambio.

Usa el endpoint abierto v6 de exchangerate-api (open.er-api.com), sin API key.
La respuesta cruda del proveedor se normaliza a `ExchangeRatesSnapshot` para
que el resto de la app no dependa de su shape específico.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import requests
import truststore
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from financial_report.config import (
    EXCHANGE_RATE_API_URL,
    MAX_RETRIES,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_BACKOFF_SECONDS,
)
from financial_report.models import ExchangeRatesSnapshot

# Usa el almacén de certificados del sistema operativo en lugar del bundle
# embebido de certifi. Necesario en redes corporativas con inspección TLS
# (proxy MITM) cuyo certificado raíz sólo está confiado por el OS, no por certifi.
truststore.inject_into_ssl()

logger = logging.getLogger(__name__)


class ExchangeAPIError(Exception):
    """Se lanza cuando no se pueden obtener tipos de cambio frescos de la API."""


def _build_session() -> requests.Session:
    """Sesión con reintentos automáticos ante fallos transitorios (timeouts, 5xx)."""
    session = requests.Session()
    retry = Retry(
        total=MAX_RETRIES,
        backoff_factor=RETRY_BACKOFF_SECONDS,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def fetch_rates() -> ExchangeRatesSnapshot:
    """Obtiene y normaliza los tipos de cambio actuales del USD.

    Lanza ExchangeAPIError ante cualquier problema de red, timeout, respuesta
    de error o payload inválido, para que el llamador pueda decidir si usa
    el fallback del historial.
    """
    session = _build_session()
    try:
        response = session.get(EXCHANGE_RATE_API_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        logger.warning("Fallo al conectar con la API de tipos de cambio: %s", exc)
        raise ExchangeAPIError(f"No se pudo conectar a la API de tipos de cambio: {exc}") from exc
    except ValueError as exc:
        logger.warning("La API devolvió un payload no-JSON inválido: %s", exc)
        raise ExchangeAPIError(f"La API devolvió un payload no-JSON inválido: {exc}") from exc

    if payload.get("result") != "success":
        error_type = payload.get("error-type", "desconocido")
        logger.warning("La API devolvió un resultado no exitoso: %s", error_type)
        raise ExchangeAPIError(f"La API devolvió un resultado no exitoso: {error_type}")

    rates = payload.get("rates")
    if not isinstance(rates, dict):
        raise ExchangeAPIError("La respuesta de la API no contiene un campo 'rates' válido")

    source_updated_at: datetime | None = None
    unix_ts = payload.get("time_last_update_unix")
    if isinstance(unix_ts, (int, float)):
        source_updated_at = datetime.fromtimestamp(unix_ts, tz=timezone.utc)

    logger.info(
        "Tasas obtenidas de la API (%d monedas, actualizadas por el proveedor: %s)",
        len(rates),
        source_updated_at,
    )
    return ExchangeRatesSnapshot(
        base=payload.get("base_code", "USD"),
        rates=rates,
        source_updated_at=source_updated_at,
    )
