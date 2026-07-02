from financial_report.simulator import (
    MAX_VARIATION,
    MIN_VARIATION,
    apply_variation,
    random_variation,
)


def test_random_variation_within_bounds():
    for _ in range(1000):
        variation = random_variation()
        assert MIN_VARIATION <= variation <= MAX_VARIATION


def test_apply_variation_positive():
    assert apply_variation(100, 0.05) == 105


def test_apply_variation_negative():
    assert apply_variation(100, -0.05) == 95


def test_apply_variation_zero():
    assert apply_variation(100, 0) == 100
