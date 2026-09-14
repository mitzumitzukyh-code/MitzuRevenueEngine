import asyncio
from app.adapters.circle import CircleDiscoveryAdapter
from app.config import settings
from app.db import SessionLocal
from app.ledger import record_event
from app.services.ingestion import ingest

class ScoutRunner:
    def __init__(self):
        self.adapter = CircleDiscoveryAdapter(settings.circle_discovery_url)

    async def run_once(self) -> dict:
        db = SessionLocal()
        created = 0
        try:
            items = await self.adapter.discover()
            for item in items:
                _, is_new = ingest(db, item)
                created += int(is_new)
            record_event(db, kind="scan", worker="scout",
                         message=f"Circle x402 scan complete: {len(items)} seen, {created} new")
            return {"seen": len(items), "new": created}
        except Exception as exc:
            record_event(db, kind="error", worker="scout",
                         message=f"{type(exc).__name__}: {exc}", is_error=True)
            raise
        finally:
            db.close()

    async def run_forever(self):
        while True:
            try:
                await self.run_once()
            except Exception:
                pass
            await asyncio.sleep(max(settings.scout_interval_seconds, 60))
