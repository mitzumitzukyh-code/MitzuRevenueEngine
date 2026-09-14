from dataclasses import asdict, dataclass

from app.demand import MarketSignal


@dataclass(frozen=True)
class UnitEconomicsAssessment:
    category: str
    observed_revenue_per_call_usd: float
    estimated_variable_cost_per_call_usd: float
    gross_margin_per_call_usd: float
    gross_margin_pct: float
    source_cost_status: str
    verdict: str
    reason: str


def assess_unit_economics(
    *,
    category: str,
    signal: MarketSignal,
    estimated_variable_cost_per_call_usd: float | None,
    source_cost_status: str,
) -> UnitEconomicsAssessment:
    revenue = (
        signal.volume_30d_usd / signal.transactions_30d
        if signal.transactions_30d > 0
        else 0.0
    )
    if estimated_variable_cost_per_call_usd is None or source_cost_status != "VERIFIED":
        return UnitEconomicsAssessment(
            category=category,
            observed_revenue_per_call_usd=round(revenue, 6),
            estimated_variable_cost_per_call_usd=0.0,
            gross_margin_per_call_usd=0.0,
            gross_margin_pct=0.0,
            source_cost_status=source_cost_status,
            verdict="RESEARCH",
            reason="Variable source cost is not independently verified.",
        )

    cost = max(0.0, estimated_variable_cost_per_call_usd)
    margin = revenue - cost
    margin_pct = (margin / revenue * 100) if revenue > 0 else 0.0
    if revenue <= 0 or margin <= 0:
        verdict = "REJECT"
        reason = "Observed market revenue does not cover verified variable cost."
    elif margin_pct >= 60:
        verdict = "PROTOTYPE"
        reason = "Verified variable cost leaves at least 60% gross margin before fixed infrastructure."
    else:
        verdict = "WATCH"
        reason = "Positive gross margin exists, but margin is below the prototype gate."

    return UnitEconomicsAssessment(
        category=category,
        observed_revenue_per_call_usd=round(revenue, 6),
        estimated_variable_cost_per_call_usd=round(cost, 6),
        gross_margin_per_call_usd=round(margin, 6),
        gross_margin_pct=round(margin_pct, 2),
        source_cost_status=source_cost_status,
        verdict=verdict,
        reason=reason,
    )


def assessment_dict(value: UnitEconomicsAssessment) -> dict:
    return asdict(value)
