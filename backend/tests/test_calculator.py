import pytest

from delivery_earnings.calculator import compute_ingreso_estimado, compute_señal


def test_ejemplo_info_md():
    ingreso_estimado, multiplicador_total = compute_ingreso_estimado(
        ingreso_base=20.0, factor_climatico=0.20, factor_demanda=0.67
    )
    assert ingreso_estimado == pytest.approx(40.08, abs=0.01)
    assert compute_señal(multiplicador_total) == "⬆ Ventana de alta oportunidad"


@pytest.mark.parametrize(
    "multiplicador_total,esperado",
    [
        (2.0, "⬆ Ventana de alta oportunidad"),
        (1.5, "⬆ Ventana de alta oportunidad"),
        (1.3, "↗ Buen momento para conectarte"),
        (1.0, "→ Momento neutro"),
        (0.9, "→ Momento neutro"),
        (0.5, "↓ Baja oportunidad, considera esperar"),
    ],
)
def test_compute_señal_umbrales(multiplicador_total, esperado):
    assert compute_señal(multiplicador_total) == esperado
