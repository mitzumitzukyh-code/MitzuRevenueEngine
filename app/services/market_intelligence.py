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


def research_candidate(db: Session, category: str) -> dict | None:
    signal = latest_signal(db, category)
    if not signal:
        return None
    scored = evaluate(signal)
    flags = classify_market(signal, scored)
    if scored.decision != "WATCH":
        return None
    if "PROVEN_DEMAND" not in flags or "SATURATED" in flags:
        return None
    leaders = db.scalars(
        select(OpportunityRecord)
        .where(
            OpportunityRecord.category == category,
            OpportunityRecord.source == "coinbase_bazaar",
        )
        .order_by(OpportunityRecord.calls_30d.desc())
        .limit(5)
    ).all()
    top_services = [{
        "provider": row.provider,
        "title": row.title,
        "url": row.url,
        "calls_30d": row.calls_30d,
        "unique_payers_30d": row.unique_payers_30d,
        "estimated_volume_30d_usd": row.estimated_volume_30d_usd,
    } for row in leaders]
    return {
        "category": category,
        "signal": asdict(signal),
        "scores": asdict(scored),
        "flags": flags,
        "top_services": top_services,
        "reason": (
            f"Proven demand with {signal.competitors} competitors; "
            f"opportunity score {scored.opportunity}. Requires unit-economics research."
        ),
    }


def research_priority(candidate: dict) -> dict:
    signal = candidate["signal"]
    services = candidate["top_services"]
    total_calls = max(int(signal["transactions_30d"]), 1)
    total_volume = float(signal["volume_30d_usd"])
    leader_calls = int(services[0]["calls_30d"]) if services else 0
    avg_revenue_per_call = total_volume / total_calls
    leader_share = leader_calls / total_calls
    concentration_penalty = round(leader_share * 25)
    monetization_score = min(100, round(avg_revenue_per_call * 10000))
    priority_score = max(
        0,
        min(
            100,
            round(
                candidate["scores"]["opportunity"] * 0.65
                + monetization_score * 0.35
                - concentration_penalty
            ),
        ),
    )
    return {
        **candidate,
        "research_metrics": {
            "avg_revenue_per_call_usd": round(avg_revenue_per_call, 6),
            "leader_call_share": round(leader_share, 4),
            "concentration_penalty": concentration_penalty,
            "monetization_score": monetization_score,
            "research_priority_score": priority_score,
        },
        "next_action": "UNIT_ECONOMICS_RESEARCH",
    }
