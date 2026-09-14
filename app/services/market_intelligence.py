from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.demand import DemandScore, MarketSignal, evaluate
from app.models import MarketMetric, OpportunityRecord

def category_competitors(db: Session, category: str) -> int:
    return db.scalar(
        select(func.count()).select_from(OpportunityRecord)
        .where(OpportunityRecord.category == category)
    ) or 0

def latest_signal(db: Session, category: str) -> MarketSignal | None:
    row = db.scalars(
        select(MarketMetric)
        .where(MarketMetric.category == category)
        .order_by(MarketMetric.created_at.desc())
        .limit(1)
    ).first()
    if not row:
        return None
    return MarketSignal(
        buyers_30d=row.buyers_30d,
        transactions_30d=row.transactions_30d,
        volume_30d_usd=row.volume_30d_usd,
        competitors=category_competitors(db, category),
    )

def score_category(db: Session, category: str) -> DemandScore | None:
    signal = latest_signal(db, category)
    return evaluate(signal) if signal else None
