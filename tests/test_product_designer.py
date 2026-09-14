from app.demand import MarketSignal
from app.product_designer import design


def test_product_plan_has_positive_margin():
    plan = design("data", MarketSignal(50, 1000, 100, 3))
    assert plan.unit_price_usd > plan.estimated_unit_cost_usd
    assert plan.gross_margin_pct > 0
    assert plan.projected_monthly_profit_usd >= 0


def test_product_plan_is_bounded():
    plan = design("search", MarketSignal(100, 1000000, 1000000, 1))
    assert 0.001 <= plan.unit_price_usd <= 1.0
    assert 100 <= plan.target_monthly_calls <= 10000
