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
                record_event(
                    db,
                    kind="market_scan",
                    worker="market",
                    message=f"{adapter.name} scan complete: {len(items)} seen, {created} new",
                )

            categories = rebuild_coinbase_category_metrics(db)
            record_event(
                db,
                kind="demand_refresh",
                worker="market",
                message=f"Coinbase demand metrics refreshed for {categories} categories",
            )
            return summary
        except Exception as exc:
            record_event(
                db,
                kind="error",
                worker="market",
                message=f"{type(exc).__name__}: {exc}",
                is_error=True,
            )
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
