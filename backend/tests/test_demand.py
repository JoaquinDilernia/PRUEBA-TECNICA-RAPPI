from delivery_earnings.demand import simulate_demand


def test_simulate_demand_dentro_de_rangos_esperados():
    for _ in range(200):
        nivel, activos, factor_demanda = simulate_demand(tipico=100)
        assert nivel in ("alta", "media", "baja")
        assert activos >= 1
        if nivel == "alta":
            assert 55 <= activos <= 80
            assert factor_demanda > 0
        elif nivel == "media":
            assert 90 <= activos <= 110
        elif nivel == "baja":
            assert 120 <= activos <= 170
            assert factor_demanda < 0


def test_simulate_demand_formula_consistente():
    _, activos, factor_demanda = simulate_demand(tipico=100)
    assert factor_demanda == (100 / activos) - 1
