import asyncio
from app.adapters.open402 import Open402DirectoryAdapter
from app.config import settings
from app.db import SessionLocal
from app.ledger import record_event
from app.services.ingestion import ingest

class MarketRunner:
    def __init__(self):
        self.adapter = Open402DirectoryAdapter(settings.open402_directory_url)

    async def run_once(self):
        db = SessionLocal()
        try:
            items = await self.adapter.discover()
            created = 0
            for item in items:
                _, is_new = ingest(db, item)
                created += int(is_new)
            record_event(db, kind="market_scan", worker="market",
                         message=f"Open402 scan complete: {len(items)} seen, {created} new")
            return {"seen": len(items), "new": created}
        except Exception as exc:
            record_event(db, kind="error", worker="market",
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
            await asyncio.sleep(max(settings.market_scan_interval_seconds, 300))
