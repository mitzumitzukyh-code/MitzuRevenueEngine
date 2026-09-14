from dataclasses import asdict

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


def classify_market(signal: MarketSignal, scored: DemandScore) -> list[str]:
    flags = []
    if signal.buyers_30d < 2 or signal.transactions_30d < 5 or signal.volume_30d_usd <= 0:
        flags.append("DEAD")
    if signal.competitors >= 25 and scored.competition >= 80:
        flags.append("SATURATED")
    if signal.buyers_30d >= 10 and signal.transactions_30d >= 50:
        flags.append("PROVEN_DEMAND")
    if scored.decision == "BUILD":
        flags.append("BUILD_CANDIDATE")
    return flags

def build_candidate(db: Session, category: str) -> dict | None:
    signal = latest_signal(db, category)
    if not signal:
        return None
    scored = evaluate(signal)
    flags = classify_market(signal, scored)
    if scored.decision != "BUILD":
        return None
    reason = (
        f"{signal.buyers_30d} buyers, {signal.transactions_30d} calls, "
        f"${signal.volume_30d_usd:.2f} estimated 30d volume, "
        f"{signal.competitors} listed competitors"
    )
    return {
        "category": category,
        "signal": asdict(signal),
        "scores": asdict(scored),
        "flags": flags,
        "reason": reason,
    }
