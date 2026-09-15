"""Commercial-readiness gate for validated sandbox products.

A technical PASS is necessary but insufficient for sale. This module keeps
commercial promotion blocked until product truthfulness, pricing evidence,
cost coverage, and payment integration are independently satisfied.
"""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CommercialReadiness:
    product: str
    technical_validation: str
    methodology_truthful: bool
    observed_market_demand: bool
    source_cost_verified: bool
    fixed_costs_accounted: bool
    pricing_validated: bool
    payment_path_validated: bool
    verdict: str
    blockers: list[str]


def assess_commercial_readiness(
    *,
    product: str,
    technical_validation: str,
    methodology_truthful: bool,
    observed_market_demand: bool,
    source_cost_verified: bool,
    fixed_costs_accounted: bool = False,
    pricing_validated: bool = False,
    payment_path_validated: bool = False,
) -> dict:
    checks = {
        "technical_validation": technical_validation == "PASS",
        "methodology_truthful": methodology_truthful,
        "observed_market_demand": observed_market_demand,
        "source_cost_verified": source_cost_verified,
        "fixed_costs_accounted": fixed_costs_accounted,
        "pricing_validated": pricing_validated,
        "payment_path_validated": payment_path_validated,
    }
    blockers = [name for name, passed in checks.items() if not passed]
    verdict = "SELLABLE" if not blockers else "NOT_SELLABLE"
    return asdict(CommercialReadiness(
        product=product,
        technical_validation=technical_validation,
        methodology_truthful=methodology_truthful,
        observed_market_demand=observed_market_demand,
        source_cost_verified=source_cost_verified,
        fixed_costs_accounted=fixed_costs_accounted,
        pricing_validated=pricing_validated,
        payment_path_validated=payment_path_validated,
        verdict=verdict,
        blockers=blockers,
    ))
