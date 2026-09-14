"""Read-only Open 402 Directory adapter.

Open 402 aggregates machine-readable manifests and on-chain verification.
This adapter is intentionally tolerant of additive schema changes.
"""
import hashlib
import httpx
from app.adapters.base import DiscoveredOpportunity

class Open402DirectoryAdapter:
    name = "open402"

    def __init__(self, directory_url: str):
        self.directory_url = directory_url

    async def discover(self) -> list[DiscoveredOpportunity]:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(self.directory_url)
            response.raise_for_status()
            payload = response.json()
        items = payload if isinstance(payload, list) else (
            payload.get("items") or payload.get("domains") or payload.get("results") or []
        )
        found = []
        for item in items:
            if not isinstance(item, dict):
                continue
            domain = str(item.get("domain") or item.get("origin") or "")
            if not domain:
                continue
            title = str(item.get("display_name") or item.get("name") or domain)
            description = str(item.get("description") or "")
            category = str(item.get("category") or "")
            payout = str(item.get("payout_address") or "")
            external_id = "open402:" + hashlib.sha256(domain.encode()).hexdigest()[:32]
            found.append(DiscoveredOpportunity(
                source=self.name,
                external_id=external_id,
                title=(title + (" · " + description if description else ""))[:500],
                url="https://" + domain,
                automation_score=100,
                category=category,
                provider=title,
                pay_to=payout,
            ))
        return found
