"""Transparent break-even model for candidate data products."""
from dataclasses import asdict, dataclass
import math


@dataclass(frozen=True)
class BreakEvenReport:
    price_per_call_usd: float
    variable_cost_per_call_usd: float
    fixed_cost_per_month_usd: float
    contribution_per_call_usd: float
    calls_to_break_even: int | None
    calls_for_first_dollar_profit: int | None
    revenue_at_break_even_usd: float | None


def calculate_break_even(
    *,
    price_per_call_usd: float,
    variable_cost_per_call_usd: float,
    fixed_cost_per_month_usd: float,
) -> dict:
    contribution = price_per_call_usd - variable_cost_per_call_usd
    if contribution <= 0:
        be = None
        first = None
        revenue = None
    else:
        be = math.ceil(max(0.0, fixed_cost_per_month_usd) / contribution)
        first = math.ceil((max(0.0, fixed_cost_per_month_usd) + 1.0) / contribution)
        revenue = round(be * price_per_call_usd, 2)
    return asdict(BreakEvenReport(
        price_per_call_usd=price_per_call_usd,
        variable_cost_per_call_usd=variable_cost_per_call_usd,
        fixed_cost_per_month_usd=fixed_cost_per_month_usd,
        contribution_per_call_usd=round(contribution, 6),
        calls_to_break_even=be,
        calls_for_first_dollar_profit=first,
        revenue_at_break_even_usd=revenue,
    ))
