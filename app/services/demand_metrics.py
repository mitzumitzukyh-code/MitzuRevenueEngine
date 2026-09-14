from collections import defaultdict

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import MarketMetric, OpportunityRecord

def rebuild_coinbase_category_metrics(db: Session) -> int:
    rows = db.scalars(
        select(OpportunityRecord).where(OpportunityRecord.source == "coinbase_bazaar")
    ).all()
    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {"buyers": 0, "transactions": 0, "volume": 0.0}
    )
    for row in rows:
        category = row.category or "uncategorized"
        grouped[category]["buyers"] += max(row.unique_payers_30d, 0)
        grouped[category]["transactions"] += max(row.calls_30d, 0)
        grouped[category]["volume"] += max(row.estimated_volume_30d_usd, 0)

    db.execute(delete(MarketMetric).where(MarketMetric.source == "coinbase_bazaar"))

    for category, values in grouped.items():
        db.add(MarketMetric(
            source="coinbase_bazaar",
            category=category,
            buyers_30d=int(values["buyers"]),
            transactions_30d=int(values["transactions"]),
            volume_30d_usd=round(values["volume"], 6),
        ))
    db.commit()
    return len(grouped)
