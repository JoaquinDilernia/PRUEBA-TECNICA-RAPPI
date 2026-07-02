"""Cliente para la API de tipos de cambio."""

from __future__ import annotations

import requests
import truststore

# Usa el almacén de certificados del sistema operativo en lugar del bundle
# embebido de certifi. Necesario en redes corporativas con inspección TLS
# (proxy MITM) cuyo certificado raíz sólo está confiado por el OS, no por certifi.
truststore.inject_into_ssl()

EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
REQUEST_TIMEOUT_SECONDS = 10


class ExchangeAPIError(Exception):
    """Se lanza cuando no se pueden obtener tipos de cambio frescos de la API."""


def fetch_rates() -> dict[str, float]:
    """Obtiene los tipos de cambio actuales del USD.

    Devuelve el diccionario completo `{codigo_moneda: tasa}` tal como lo
    entrega la API (sin filtrar). Lanza ExchangeAPIError ante cualquier
    problema de red, timeout, status distinto de 200 o payload inválido,
    para que el llamador pueda decidir si usa el fallback del historial.
    """
    try:
        response = requests.get(EXCHANGE_RATE_API_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise ExchangeAPIError(f"No se pudo conectar a la API de tipos de cambio: {exc}") from exc
    except ValueError as exc:
        raise ExchangeAPIError(f"La API devolvió un payload no-JSON inválido: {exc}") from exc

    rates = payload.get("rates")
    if not isinstance(rates, dict):
        raise ExchangeAPIError("La respuesta de la API no contiene un campo 'rates' válido")

    return rates
