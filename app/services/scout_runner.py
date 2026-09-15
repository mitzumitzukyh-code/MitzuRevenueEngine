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
            message = f"Circle x402 scan complete: {len(items)} seen, {created} new"
            record_event(db, kind="scan", worker="scout", message=message)
            print(message, flush=True)
            return {"seen": len(items), "new": created}
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            record_event(db, kind="error", worker="scout", message=message, is_error=True)
            print(f"Scout error: {message}", flush=True)
            raise
        finally:
            db.close()

    async def run_forever(self):
        failures = 0
        while True:
            try:
                await self.run_once()
                failures = 0
                delay = max(settings.scout_interval_seconds, 60)
            except Exception as exc:
                failures += 1
                db = SessionLocal()
                try:
                    record_event(db, kind="worker_failure", worker="scout", message=f"consecutive_failures={failures} error={type(exc).__name__}", is_error=True)
                finally:
                    db.close()
                if failures >= settings.worker_max_consecutive_failures:
                    raise RuntimeError("scout exceeded consecutive failure limit") from exc
                delay = min(2 ** failures, settings.worker_backoff_max_seconds)
            await asyncio.sleep(delay)
