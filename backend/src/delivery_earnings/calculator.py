SEÑALES = (
    (1.5, "⬆ Ventana de alta oportunidad"),
    (1.1, "↗ Buen momento para conectarte"),
    (0.9, "→ Momento neutro"),
)


def compute_señal(multiplicador_total: float) -> str:
    for umbral, texto in SEÑALES:
        if multiplicador_total >= umbral:
            return texto
    return "↓ Baja oportunidad, considera esperar"


def compute_ingreso_estimado(
    ingreso_base: float, factor_climatico: float, factor_demanda: float
) -> tuple[float, float]:
    multiplicador_total = (1 + factor_climatico) * (1 + factor_demanda)
    ingreso_estimado = ingreso_base * multiplicador_total
    return ingreso_estimado, multiplicador_total
