from app.commercial_readiness import assess_commercial_readiness
from app.demand import MarketSignal
from app.product_designer import design


def test_unknown_commercial_evidence_blocks_sale():
    result = assess_commercial_readiness(
        product="liquidations", technical_validation="UNKNOWN", methodology_truthful=None,
        observed_market_demand=None, source_cost_verified=None,
    )
    assert result["verdict"] == "NOT_SELLABLE"
    assert result["methodology_truthful"] is None
    assert "technical_validation" in result["blockers"]


def test_product_plan_does_not_invent_cost_or_call_target():
    plan = design("liquidations", MarketSignal(buyers_30d=10, transactions_30d=100, volume_30d_usd=20, competitors=3))
    assert plan.estimated_unit_cost_usd is None
    assert plan.target_monthly_calls is None
    assert plan.projected_monthly_profit_usd is None
    assert plan.projection_status == "UNKNOWN"
