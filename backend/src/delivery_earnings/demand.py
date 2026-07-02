import random

TIPICO = 100

# rango de activos como fraccion del tipico, por nivel (ver docs/SPEC.md #3)
NIVEL_RANGOS = {
    "alta": (0.55, 0.80),
    "media": (0.90, 1.10),
    "baja": (1.20, 1.70),
}

NIVELES_PESOS = {"alta": 0.33, "media": 0.34, "baja": 0.33}


def simulate_demand(tipico: int = TIPICO) -> tuple[str, int, float]:
    nivel = random.choices(
        population=list(NIVELES_PESOS.keys()),
        weights=list(NIVELES_PESOS.values()),
        k=1,
    )[0]
    low, high = NIVEL_RANGOS[nivel]
    activos = round(tipico * random.uniform(low, high))
    activos = max(activos, 1)
    factor_demanda = (tipico / activos) - 1
    return nivel, activos, factor_demanda
