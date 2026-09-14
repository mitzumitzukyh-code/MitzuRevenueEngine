from dataclasses import dataclass
from enum import StrEnum

class Decision(StrEnum):
    REJECT = "reject"
    REVIEW = "review"
    EXECUTE = "execute"

@dataclass(frozen=True)
class Opportunity:
    source: str
    title: str
    expected_revenue_usd: float
    estimated_cost_usd: float
    automation_score: int
    payment_probability: float
    success_probability: float

    @property
    def expected_profit_usd(self) -> float:
        return self.expected_revenue_usd * self.payment_probability * self.success_probability - self.estimated_cost_usd

    @property
    def roi(self) -> float:
        return self.expected_profit_usd / self.estimated_cost_usd if self.estimated_cost_usd > 0 else float("inf")
