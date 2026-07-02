"""Simulación de variación diaria de tipos de cambio."""

from __future__ import annotations

import random

MIN_VARIATION = -0.02
MAX_VARIATION = 0.02


def random_variation() -> float:
    """Variación diaria simulada, uniforme entre -2% y +2% (como fracción, ej. 0.015 = +1.5%)."""
    return random.uniform(MIN_VARIATION, MAX_VARIATION)


def apply_variation(rate: float, variation: float) -> float:
    """Aplica la variación simulada a una tasa base."""
    return rate * (1 + variation)
