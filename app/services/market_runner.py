import asyncio

from app.adapters.coinbase import CoinbaseBazaarAdapter
from app.adapters.open402 import Open402DirectoryAdapter
from app.config import settings
from app.db import SessionLocal
from app.ledger import record_event
from app.services.demand_metrics import rebuild_coinbase_category_metrics
from app.services.ingestion import ingest

class MarketRunner:
    def __init__(self):
        self.adapters = [
            Open402DirectoryAdapter(settings.open402_directory_url),
            CoinbaseBazaarAdapter(
                settings.coinbase_bazaar_url,
                settings.coinbase_page_size,
                settings.coinbase_max_pages,
            ),
        ]

    async def run_once(self):
        db = SessionLocal()
        summary = {}
        try:
            for adapter in self.adapters:
                items = await adapter.discover()
                created = 0
                for item in items:
                    _, is_new = ingest(db, item)
                    created += int(is_new)
                summary[adapter.name] = {"seen": len(items), "new": created}
                message = f"{adapter.name} scan complete: {len(items)} seen, {created} new"
                record_event(db, kind="market_scan", worker="market", message=message)
                print(message, flush=True)

            categories = rebuild_coinbase_category_metrics(db)
            message = f"Coinbase demand metrics refreshed for {categories} categories"
            record_event(db, kind="demand_refresh", worker="market", message=message)
            print(message, flush=True)
            return summary
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            record_event(db, kind="error", worker="market", message=message, is_error=True)
            print(f"Market error: {message}", flush=True)
            raise
        finally:
            db.close()

    async def run_forever(self):
        failures = 0
        while True:
            try:
                await self.run_once()
                failures = 0
                delay = max(settings.market_scan_interval_seconds, 300)
            except Exception as exc:
                failures += 1
                db = SessionLocal()
                try:
                    record_event(db, kind="worker_failure", worker="market", message=f"consecutive_failures={failures} error={type(exc).__name__}", is_error=True)
                finally:
                    db.close()
                if failures >= settings.worker_max_consecutive_failures:
                    raise RuntimeError("market exceeded consecutive failure limit") from exc
                delay = min(2 ** failures, settings.worker_backoff_max_seconds)
            await asyncio.sleep(delay)
