from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class DiscoveredOpportunity:
    source: str
    external_id: str
    title: str
    url: str = ""
    expected_revenue_usd: float = 0
    estimated_cost_usd: float = 0
    automation_score: int = 0
    payment_probability: float = 0
    success_probability: float = 0
    category: str = ""
    provider: str = ""
    network: str = ""
    asset: str = ""
    price_atomic: str = ""
    pay_to: str = ""
    calls_30d: int = 0
    unique_payers_30d: int = 0
    estimated_volume_30d_usd: float = 0

class OpportunityAdapter(Protocol):
    name: str
    async def discover(self) -> list[DiscoveredOpportunity]: ...
