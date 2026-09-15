"""Opportunity Scout v0.1.

Ranks externally discovered work without accepting jobs, spending money,
signing transactions, or handling payout credentials.
"""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Opportunity:
    source: str
    title: str
    payout_usd: float
    funded: bool
    capital_required_usd: float = 0.0
    success_probability: float = 0.0
    estimated_ai_cost_usd: float = 0.0
    risk_penalty_usd: float = 0.0
    requires_spam: bool = False
    requires_trading: bool = False
    requires_deposit: bool = False

    @property
    def expected_value_usd(self) -> float:
        return round(
            self.payout_usd * self.success_probability
            - self.estimated_ai_cost_usd
            - self.risk_penalty_usd
            - self.capital_required_usd,
            2,
        )


def eligible(job: Opportunity) -> bool:
    return bool(
        job.funded
        and job.payout_usd >= 5
        and job.capital_required_usd == 0
        and job.success_probability >= 0.70
        and not job.requires_spam
        and not job.requires_trading
        and not job.requires_deposit
    )


def rank(jobs: list[Opportunity]) -> list[dict]:
    accepted = [job for job in jobs if eligible(job)]
    accepted.sort(key=lambda job: job.expected_value_usd, reverse=True)
    return [
        {**asdict(job), "expected_value_usd": job.expected_value_usd}
        for job in accepted
    ]


SAFETY_POLICY = {
    "may_discover": True,
    "may_rank": True,
    "may_prepare_work": True,
    "may_accept_external_commitment": False,
    "may_spend": False,
    "may_sign_transaction": False,
    "may_expose_wallet_secret": False,
}
