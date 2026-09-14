from dataclasses import dataclass

@dataclass(frozen=True)
class MarketSignal:
    buyers_30d: int
    transactions_30d: int
    volume_30d_usd: float
    competitors: int

@dataclass(frozen=True)
class DemandScore:
    demand: int
    competition: int
    opportunity: int
    decision: str

def _clamp(n: float) -> int:
    return int(max(0, min(round(n), 100)))

def evaluate(signal: MarketSignal) -> DemandScore:
    buyer_signal = min(signal.buyers_30d / 50, 1) * 35
    tx_signal = min(signal.transactions_30d / 1000, 1) * 25
    volume_signal = min(signal.volume_30d_usd / 1000, 1) * 40
    demand = _clamp(buyer_signal + tx_signal + volume_signal)

    competition = _clamp(min(signal.competitors / 25, 1) * 100)
    opportunity = _clamp(demand * 0.75 + (100 - competition) * 0.25)

    if signal.buyers_30d < 2 or signal.transactions_30d < 5 or signal.volume_30d_usd <= 0:
        decision = "REJECT"
    elif opportunity >= 80:
        decision = "BUILD"
    elif opportunity >= 55:
        decision = "WATCH"
    else:
        decision = "REJECT"
    return DemandScore(demand=demand, competition=competition, opportunity=opportunity, decision=decision)
