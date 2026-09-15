from app.commercial_readiness import assess_commercial_readiness


def test_technical_pass_alone_is_not_sellable():
    result = assess_commercial_readiness(
        product="liquidations",
        technical_validation="PASS",
        methodology_truthful=True,
        observed_market_demand=True,
        source_cost_verified=True,
    )
    assert result["verdict"] == "NOT_SELLABLE"
    assert "fixed_costs_accounted" in result["blockers"]
    assert "pricing_validated" in result["blockers"]
    assert "payment_path_validated" in result["blockers"]


def test_all_gates_required_for_sellable():
    result = assess_commercial_readiness(
        product="liquidations",
        technical_validation="PASS",
        methodology_truthful=True,
        observed_market_demand=True,
        source_cost_verified=True,
        fixed_costs_accounted=True,
        pricing_validated=True,
        payment_path_validated=True,
    )
    assert result["verdict"] == "SELLABLE"
    assert result["blockers"] == []
