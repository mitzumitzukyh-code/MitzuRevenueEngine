from dataclasses import asdict

from sqlalchemy.orm import Session

from app.product_designer import design
from app.services.market_intelligence_service import build_candidate, latest_signal


def design_for_category(db: Session, category: str) -> dict | None:
    candidate = build_candidate(db, category)
    if not candidate:
        return None
    signal = latest_signal(db, category)
    if not signal:
        return None
    plan = design(category, signal)
    return {
        "candidate": candidate,
        "product": asdict(plan),
        "execution_status": "PLANNED_ONLY",
        "autonomous_deploy": False,
        "wallet_required": False,
    }
