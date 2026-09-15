from app.evaluation_lab import evaluate_blueprint
from app.product_designer import ProductPlan
from app.service_factory import build_blueprint


def _blueprint():
    return build_blueprint(ProductPlan(
        category="data", product_name="Mitzu Data API",
        unit_price_usd=0.01, estimated_unit_cost_usd=0.002,
        gross_margin_pct=80, target_monthly_calls=100,
        projected_monthly_revenue_usd=1,
        projected_monthly_cost_usd=0.2,
        projected_monthly_profit_usd=0.8, cost_basis="TEST_FIXTURE",
        projection_status="TEST_FIXTURE", rationale="test",
    ))


def test_evaluation_passes_zero_spend_runtime():
    report = evaluate_blueprint(_blueprint(), 50)
    assert report.requests == 50
    assert report.success_rate_pct == 100
    assert report.total_estimated_cost_usd == 0
    assert report.payment_attempts == 0
    assert report.verdict == "PASS"


def test_evaluation_caps_request_batch():
    report = evaluate_blueprint(_blueprint(), 5000)
    assert report.requests == 1000
