from app.product_designer import ProductPlan
from app.sandbox_runtime import execute, health
from app.service_factory import build_blueprint


def _blueprint():
    return build_blueprint(ProductPlan(
        category="data",
        product_name="Mitzu Data API",
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
    ))


def test_sandbox_execution_never_attempts_payment():
    result = execute(_blueprint(), {"query": "hello"})
    assert result.status == "ok"
    assert result.estimated_cost_usd == 0
    assert result.billable is False
    assert result.payment_attempted is False


def test_sandbox_health_keeps_x402_disabled():
    result = health(_blueprint())
    assert result["status"] == "healthy"
    assert result["x402_enabled"] is False
    assert result["spending_allowed"] is False
