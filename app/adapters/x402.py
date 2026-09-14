"""x402 discovery adapter.

The adapter is deliberately read-only. It discovers public x402 resources but
has no wallet/signing capability. Provider URLs are configured, not hard-coded
into execution policy.
"""
import hashlib
import httpx
from app.adapters.base import DiscoveredOpportunity

class X402DiscoveryAdapter:
    name = "x402"

    def __init__(self, discovery_url: str):
        self.discovery_url = discovery_url

    async def discover(self) -> list[DiscoveredOpportunity]:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get(self.discovery_url)
            response.raise_for_status()
            payload = response.json()
        items = payload if isinstance(payload, list) else payload.get("items", payload.get("resources", []))
        found = []
        for item in items:
            if not isinstance(item, dict):
                continue
            url = str(item.get("url") or item.get("endpoint") or "")
            title = str(item.get("name") or item.get("title") or url or "x402 resource")
            raw_id = str(item.get("id") or url or title)
            external_id = hashlib.sha256(raw_id.encode()).hexdigest()[:32]
            found.append(DiscoveredOpportunity(source=self.name, external_id=external_id, title=title, url=url))
        return found
