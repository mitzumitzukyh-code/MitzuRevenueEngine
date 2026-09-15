"""Normalize GitHub bounty issues into Opportunity Scout candidates."""
import re
from app.opportunity_scout import BountyOpportunity

BOUNTY_RE = re.compile(r"/bounty\s+\$([0-9]+(?:\.[0-9]+)?)", re.I)


def bounty_amount(body: str) -> float | None:
    match = BOUNTY_RE.search(body or "")
    return float(match.group(1)) if match else None


def from_github_issue(
    *,
    repo: str,
    number: int,
    title: str,
    body: str,
    funded: bool,
    success_probability: float,
    estimated_ai_cost_usd: float = 0,
    risk_penalty_usd: float = 0,
) -> BountyOpportunity | None:
    amount = bounty_amount(body)
    if amount is None:
        return None
    return BountyOpportunity(
        source=f"github:{repo}#{number}",
        title=title,
        payout_usd=amount,
        funded=funded,
        success_probability=success_probability,
        estimated_ai_cost_usd=estimated_ai_cost_usd,
        risk_penalty_usd=risk_penalty_usd,
    )
