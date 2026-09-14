"""Read-only Circle Agent Marketplace discovery.

Uses Circle's public keyless x402 discovery endpoint. This adapter never signs
transactions and never receives wallet credentials.
"""
import hashlib
import httpx
from app.adapters.base import DiscoveredOpportunity

class CircleDiscoveryAdapter:
    name = "circle_x402"

    def __init__(self, discovery_url: str):
        self.discovery_url = discovery_url

    async def discover(self) -> list[DiscoveredOpportunity]:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(self.discovery_url)
            response.raise_for_status()
            payload = response.json()
        items = payload if isinstance(payload, list) else payload.get("resources", payload.get("items", []))
        found: list[DiscoveredOpportunity] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            url = str(item.get("resource") or item.get("url") or "")
            metadata = item.get("metadata") or {}
            provider = metadata.get("provider") or {}
            description = str(metadata.get("description") or provider.get("description") or "")
            provider_name = str(provider.get("name") or "")
            category = str(provider.get("category") or "")
            accepts = item.get("accepts") or []
            payment = accepts[0] if accepts and isinstance(accepts[0], dict) else {}
            network = str(payment.get("network") or "")
            asset = str(payment.get("asset") or "")
            price_atomic = str(payment.get("amount") or "")
            pay_to = str(payment.get("payTo") or "")
            title = " · ".join(x for x in (provider_name, description) if x) or url or "x402 service"
            raw_id = url or title
            external_id = "circle:" + hashlib.sha256(raw_id.encode()).hexdigest()[:32]
            found.append(DiscoveredOpportunity(
                source=self.name, external_id=external_id, title=title, url=url,
                automation_score=100, category=category, provider=provider_name,
                network=network, asset=asset, price_atomic=price_atomic, pay_to=pay_to,
            ))
        return found
