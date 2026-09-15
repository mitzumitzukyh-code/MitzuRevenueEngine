from dataclasses import dataclass

from app.demand import MarketSignal


@dataclass(frozen=True)
class ProductPlan:
    category: str
    product_name: str
    unit_price_usd: float
    estimated_unit_cost_usd: float | None
    cost_basis: str
    gross_margin_pct: float | None
    target_monthly_calls: int | None
    projected_monthly_revenue_usd: float | None
    projected_monthly_cost_usd: float | None
    projected_monthly_profit_usd: float | None
    projection_status: str
    rationale: str


def _price_from_market(signal: MarketSignal) -> float:
    if signal.transactions_30d <= 0 or signal.volume_30d_usd <= 0:
        return 0.01
    observed_avg = signal.volume_30d_usd / signal.transactions_30d
    return max(0.001, min(round(observed_avg * 0.85, 6), 1.0))


def design(category: str, signal: MarketSignal) -> ProductPlan:
    price = _price_from_market(signal)
    clean = category.strip() or "General"
    return ProductPlan(
        category=clean,
        product_name=f"Mitzu {clean.title()} API",
        unit_price_usd=price,
        estimated_unit_cost_usd=None,
        cost_basis="UNKNOWN_UNTIL_MEASURED",
        gross_margin_pct=None,
        target_monthly_calls=None,
        projected_monthly_revenue_usd=None,
        projected_monthly_cost_usd=None,
        projected_monthly_profit_usd=None,
        projection_status="UNKNOWN",
        rationale="Price is derived from observed market transaction economics; costs and demand targets remain UNKNOWN until measured.",
    )
