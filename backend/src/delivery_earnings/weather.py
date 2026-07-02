import ssl

import httpx
import truststore

from .config import WEATHER_API_BASE_URL, WEATHER_API_KEY
from .models import Vehiculo

_SSL_CONTEXT = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# demand_shift base por categoria climatica (ver docs/SPEC.md #2.2)
DEMAND_SHIFT = {
    "despejado": 0.00,
    "lluvia": 0.20,
    "tormenta_nieve": 0.30,
    "viento_fuerte": 0.10,
    "calor_extremo": 0.10,
    "frio_extremo": 0.15,
}

# modificador de operatividad por vehiculo y categoria (ver docs/SPEC.md #2.3)
OPERABILITY_MOD = {
    "despejado": {Vehiculo.moto: 0.00, Vehiculo.bici: 0.00, Vehiculo.auto: 0.00},
    "lluvia": {Vehiculo.moto: 0.00, Vehiculo.bici: -0.10, Vehiculo.auto: 0.05},
    "tormenta_nieve": {Vehiculo.moto: -0.25, Vehiculo.bici: -0.40, Vehiculo.auto: -0.10},
    "viento_fuerte": {Vehiculo.moto: -0.10, Vehiculo.bici: -0.20, Vehiculo.auto: 0.00},
    "calor_extremo": {Vehiculo.moto: -0.15, Vehiculo.bici: -0.15, Vehiculo.auto: -0.05},
    "frio_extremo": {Vehiculo.moto: -0.10, Vehiculo.bici: -0.20, Vehiculo.auto: 0.00},
}

_STORM_SNOW_KEYWORDS = ("snow", "sleet", "blizzard", "thunder")
_RAIN_KEYWORDS = ("rain", "drizzle", "shower")


def classify_weather(condition_text: str, temp_c: float, wind_kph: float, precip_mm: float) -> str:
    text = condition_text.lower()

    if any(k in text for k in _STORM_SNOW_KEYWORDS) or precip_mm > 10:
        return "tormenta_nieve"
    if any(k in text for k in _RAIN_KEYWORDS) or precip_mm > 0.5:
        return "lluvia"
    if wind_kph > 40:
        return "viento_fuerte"
    if temp_c > 35:
        return "calor_extremo"
    if temp_c < 5:
        return "frio_extremo"
    return "despejado"


def compute_factor_climatico(categoria: str, vehiculo: Vehiculo) -> tuple[float, float, float]:
    demand_shift = DEMAND_SHIFT[categoria]
    operability_mod = OPERABILITY_MOD[categoria][vehiculo]
    return demand_shift, operability_mod, demand_shift + operability_mod


async def fetch_current_weather(lat: float, lon: float) -> dict:
    async with httpx.AsyncClient(
        base_url=WEATHER_API_BASE_URL, timeout=10.0, verify=_SSL_CONTEXT
    ) as client:
        response = await client.get(
            "/current.json",
            params={"key": WEATHER_API_KEY, "q": f"{lat},{lon}"},
        )
        response.raise_for_status()
        return response.json()
