from app.product_designer import ProductPlan
from app.service_factory import build_blueprint


def test_blueprint_is_sandboxed_and_unpaid():
    plan = ProductPlan(
        category="data",
        product_name="Mitzu Data API",
        unit_price_usd=0.01,
        estimated_unit_cost_usd=0.002,
        gross_margin_pct=80,
        target_monthly_calls=1000,
        projected_monthly_revenue_usd=10,
        projected_monthly_cost_usd=2,
        projected_monthly_profit_usd=8,
        cost_basis="TEST_FIXTURE",
        projection_status="TEST_FIXTURE",
        rationale="test",
    )
    blueprint = build_blueprint(plan)
    assert blueprint.sandbox_only is True
    assert blueprint.autonomous_deploy is False
    assert blueprint.manifest["x402"]["enabled"] is False
    assert blueprint.manifest["safety"]["spending_allowed"] is False


def test_blueprint_generates_stable_route():
    plan = ProductPlan(
        category="search",
        product_name="Mitzu Search API",
        unit_price_usd=0.01,
        estimated_unit_cost_usd=0.002,
        gross_margin_pct=80,
        target_monthly_calls=100,
        projected_monthly_revenue_usd=1,
        projected_monthly_cost_usd=0.2,
        projected_monthly_profit_usd=0.8,
        cost_basis="TEST_FIXTURE",
        projection_status="TEST_FIXTURE",
        rationale="test",
    )
    blueprint = build_blueprint(plan)
    assert blueprint.route == "/services/mitzu-search-api"
    assert blueprint.health_route == "/services/mitzu-search-api/health"
