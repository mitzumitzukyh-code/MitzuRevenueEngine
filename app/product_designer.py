from dataclasses import dataclass

from app.demand import MarketSignal


@dataclass(frozen=True)
class ProductPlan:
    category: str
    product_name: str
    unit_price_usd: float
    estimated_unit_cost_usd: float
    gross_margin_pct: float
    target_monthly_calls: int
    projected_monthly_revenue_usd: float
    projected_monthly_cost_usd: float
    projected_monthly_profit_usd: float
    rationale: str


def _pricing_from_market(signal: MarketSignal) -> tuple[float, float]:
    if signal.transactions_30d <= 0 or signal.volume_30d_usd <= 0:
        return 0.01, 0.002
    observed_avg = signal.volume_30d_usd / signal.transactions_30d
    price = max(0.001, min(round(observed_avg * 0.85, 6), 1.0))
    cost = max(0.0001, min(round(price * 0.2, 6), price * 0.5))
    return price, cost


def design(category: str, signal: MarketSignal) -> ProductPlan:
    price, cost = _pricing_from_market(signal)
    target_calls = max(100, min(signal.transactions_30d // max(signal.competitors, 1), 10000))
    revenue = round(target_calls * price, 2)
    monthly_cost = round(target_calls * cost, 2)
    profit = round(revenue - monthly_cost, 2)
    margin = round(((price - cost) / price) * 100, 1) if price > 0 else 0.0
    clean = category.strip() or "General"
    product_name = f"Mitzu {clean.title()} API"
    rationale = (
        f"Targets {target_calls} calls/month at $" + f"{price:.4f}/call with "
        f"estimated {margin:.1f}% gross margin based on observed category economics."
    )
    return ProductPlan(
        category=clean,
        product_name=product_name,
        unit_price_usd=price,
        estimated_unit_cost_usd=cost,
        gross_margin_pct=margin,
        target_monthly_calls=target_calls,
        projected_monthly_revenue_usd=revenue,
        projected_monthly_cost_usd=monthly_cost,
        projected_monthly_profit_usd=profit,
        rationale=rationale,
    )
