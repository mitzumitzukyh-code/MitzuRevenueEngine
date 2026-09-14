"""Read-only Open 402 Directory adapter.

Open 402 aggregates machine-readable manifests and on-chain verification.
This adapter is intentionally tolerant of additive schema changes.
"""
import hashlib
import httpx
from app.adapters.base import DiscoveredOpportunity


def _directory_items(payload) -> list[dict]:
    """Normalize known directory response envelopes without weakening validation."""
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []

    candidates = [
        payload.get("items"),
        payload.get("domains"),
        payload.get("results"),
        payload.get("entries"),
        payload.get("services"),
        payload.get("data"),
    ]
    for candidate in candidates:
        if isinstance(candidate, list):
            return [item for item in candidate if isinstance(item, dict)]
        if isinstance(candidate, dict):
            nested = _directory_items(candidate)
            if nested:
                return nested
    return []


class Open402DirectoryAdapter:
    name = "open402"

    def __init__(self, directory_url: str):
        self.directory_url = directory_url

    async def discover(self) -> list[DiscoveredOpportunity]:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(self.directory_url)
            response.raise_for_status()
            payload = response.json()

        items = _directory_items(payload)
        found = []
        for item in items:
            domain = str(
                item.get("domain")
                or item.get("origin")
                or item.get("hostname")
                or item.get("host")
                or ""
            ).strip()
            if not domain:
                continue
            domain = domain.removeprefix("https://").removeprefix("http://").rstrip("/")
            title = str(item.get("display_name") or item.get("displayName") or item.get("name") or domain)
            description = str(item.get("description") or "")
            category = str(item.get("category") or "")
            payout = str(item.get("payout_address") or item.get("payoutAddress") or "")
            external_id = "open402:" + hashlib.sha256(domain.encode()).hexdigest()[:32]
            found.append(DiscoveredOpportunity(
                source=self.name,
                external_id=external_id,
                title=(title + (" · " + description if description else ""))[:500],
                url="https://" + domain,
                automation_score=100,
                category=category[:80],
                provider=title[:200],
                pay_to=payout[:200],
            ))
        return found
