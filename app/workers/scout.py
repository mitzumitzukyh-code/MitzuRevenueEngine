"""Opportunity discovery worker.

Adapters are intentionally isolated from decision/execution logic so sources can
be added or disabled without granting them spending or wallet privileges.
"""

class Scout:
    async def scan(self) -> list[dict]:
        return []
