import pytest

from delivery_earnings.models import Vehiculo
from delivery_earnings.weather import classify_weather, compute_factor_climatico


@pytest.mark.parametrize(
    "condition_text,temp_c,wind_kph,precip_mm,esperado",
    [
        ("Sunny", 22.0, 10.0, 0.0, "despejado"),
        ("Patchy rain nearby", 18.0, 10.0, 1.0, "lluvia"),
        ("Light drizzle", 18.0, 10.0, 0.0, "lluvia"),
        ("Moderate snow", -2.0, 10.0, 15.0, "tormenta_nieve"),
        ("Thundery outbreaks possible", 20.0, 10.0, 0.0, "tormenta_nieve"),
        ("Clear", 20.0, 50.0, 0.0, "viento_fuerte"),
        ("Clear", 38.0, 10.0, 0.0, "calor_extremo"),
        ("Clear", 2.0, 10.0, 0.0, "frio_extremo"),
    ],
)
def test_classify_weather(condition_text, temp_c, wind_kph, precip_mm, esperado):
    assert classify_weather(condition_text, temp_c, wind_kph, precip_mm) == esperado


def test_factor_climatico_ejemplo_info_md():
    # moto + lluvia debe dar +20% segun el ejemplo del info.md
    demand_shift, operability_mod, factor = compute_factor_climatico("lluvia", Vehiculo.moto)
    assert demand_shift == 0.20
    assert operability_mod == 0.00
    assert factor == pytest.approx(0.20)


def test_factor_climatico_bici_penalizada_mas_que_moto_en_lluvia():
    _, _, factor_moto = compute_factor_climatico("lluvia", Vehiculo.moto)
    _, _, factor_bici = compute_factor_climatico("lluvia", Vehiculo.bici)
    assert factor_bici < factor_moto


def test_factor_climatico_auto_menos_penalizado_en_tormenta():
    _, _, factor_auto = compute_factor_climatico("tormenta_nieve", Vehiculo.auto)
    _, _, factor_bici = compute_factor_climatico("tormenta_nieve", Vehiculo.bici)
    assert factor_auto > factor_bici
