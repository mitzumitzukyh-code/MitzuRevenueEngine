"""Public Coinbase Bazaar discovery adapter.

Uses the unauthenticated discovery API and its 30-day quality counters.
No payment headers, wallet keys, signing, or settlement code exist here.
"""
import hashlib
from urllib.parse import urlparse

import httpx

from app.adapters.base import DiscoveredOpportunity

_USDC_ASSETS = {
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    "0x036cbd53842c5426634e7929541ec2318f3dcf7e",
    "epjfwdd5aufqssq2ibtwgsp8vdtdaaqbby1vz9ppump",
}

def _usd_price(payment: dict) -> float:
    amount = payment.get("amount")
    asset = str(payment.get("asset") or "").lower()
    extra = payment.get("extra") or {}
    is_usdc = asset in _USDC_ASSETS or "usd coin" in str(extra.get("name") or "").lower()
    if not is_usdc:
        return 0.0
    try:
        return int(str(amount)) / 1_000_000
    except (TypeError, ValueError):
        return 0.0

class CoinbaseBazaarAdapter:
    name = "coinbase_bazaar"

    def __init__(self, base_url: str, page_size: int = 100, max_pages: int = 200):
        self.base_url = base_url
        self.page_size = max(1, min(page_size, 1000))
        self.max_pages = max(1, max_pages)

    async def discover(self) -> list[DiscoveredOpportunity]:
        offset = 0
        pages = 0
        found: list[DiscoveredOpportunity] = []
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            while pages < self.max_pages:
                response = await client.get(
                    self.base_url,
                    params={"limit": self.page_size, "offset": offset},
                )
                response.raise_for_status()
                payload = response.json()
                items = payload.get("items", []) if isinstance(payload, dict) else []
                if not items:
                    break
                for item in items:
                    resource = str(item.get("resource") or "")
                    if not resource:
                        continue
                    quality = item.get("quality") or {}
                    accepts = item.get("accepts") or []
                    payment = accepts[0] if accepts and isinstance(accepts[0], dict) else {}
                    price_usd = _usd_price(payment)
                    calls = int(quality.get("l30DaysTotalCalls") or 0)
                    payers = int(quality.get("l30DaysUniquePayers") or 0)
                    tags = item.get("tags") or []
                    category = str(tags[0]) if tags else "uncategorized"
                    service_name = str(item.get("serviceName") or urlparse(resource).netloc or resource)
                    description = str(item.get("description") or "")
                    external_id = "coinbase:" + hashlib.sha256(resource.encode()).hexdigest()[:32]
                    found.append(DiscoveredOpportunity(
                        source=self.name,
                        external_id=external_id,
                        title=(service_name + (" · " + description if description else ""))[:500],
                        url=resource,
                        automation_score=100,
                        category=category[:80],
                        provider=service_name[:200],
                        network=str(payment.get("network") or ""),
                        asset=str(payment.get("asset") or ""),
                        price_atomic=str(payment.get("amount") or ""),
                        pay_to=str(payment.get("payTo") or ""),
                        calls_30d=max(calls, 0),
                        unique_payers_30d=max(payers, 0),
                        estimated_volume_30d_usd=round(max(calls, 0) * price_usd, 6),
                    ))
                pages += 1
                pagination = payload.get("pagination") or {}
                total = int(pagination.get("total") or 0)
                offset += len(items)
                if len(items) < self.page_size or (total and offset >= total):
                    break
        return found
