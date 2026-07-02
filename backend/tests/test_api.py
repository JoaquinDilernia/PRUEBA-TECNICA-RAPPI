import pytest
import respx
from httpx import ASGITransport, AsyncClient, Response

from delivery_earnings.api import app
from delivery_earnings.config import WEATHER_API_BASE_URL


@pytest.mark.asyncio
@respx.mock
async def test_potencial_ingresos_lluvia_moto():
    respx.get(f"{WEATHER_API_BASE_URL}/current.json").mock(
        return_value=Response(
            200,
            json={
                "current": {
                    "condition": {"text": "Patchy rain nearby"},
                    "temp_c": 18.0,
                    "wind_kph": 10.0,
                    "precip_mm": 1.0,
                }
            },
        )
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/potencial-ingresos",
            json={"ingreso_base": 20.0, "vehiculo": "moto", "lat": -34.6, "lon": -58.4},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["clima"]["categoria"] == "lluvia"
    assert data["clima"]["factor_climatico"] == pytest.approx(0.20)
    assert data["demanda"]["nivel"] in ("alta", "media", "baja")
    assert data["ingreso_estimado"] > 0
    assert "señal" in data


@pytest.mark.asyncio
@respx.mock
async def test_potencial_ingresos_valida_vehiculo_invalido():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/potencial-ingresos",
            json={"ingreso_base": 20.0, "vehiculo": "camion", "lat": -34.6, "lon": -58.4},
        )

    assert response.status_code == 422
