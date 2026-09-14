from dataclasses import dataclass
from app.domain import Opportunity

@dataclass(frozen=True)
class Score:
    value: int
    expected_profit_usd: float
    roi: float

def score(op: Opportunity) -> Score:
    # Conservative 0-100 score: automation and payment certainty dominate.
    profit_signal = min(max(op.expected_profit_usd, 0) / 10, 1) * 20
    roi_signal = min(max(op.roi, 0) / 10, 1) * 15
    automation_signal = min(max(op.automation_score, 0), 100) * 0.35
    payment_signal = min(max(op.payment_probability, 0), 1) * 20
    success_signal = min(max(op.success_probability, 0), 1) * 10
    value = round(profit_signal + roi_signal + automation_signal + payment_signal + success_signal)
    return Score(min(max(value, 0), 100), round(op.expected_profit_usd, 4), round(op.roi, 4))
