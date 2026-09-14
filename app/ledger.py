from sqlalchemy.orm import Session
from app.models import ActivityEvent, LedgerEntry

def record_event(db: Session, *, kind: str, worker: str, message: str,
                 opportunity_id: int | None = None, amount_usd: float = 0,
                 is_error: bool = False, recovered: bool = False) -> ActivityEvent:
    event = ActivityEvent(kind=kind, worker=worker, message=message,
                          opportunity_id=opportunity_id, amount_usd=amount_usd,
                          is_error=is_error, recovered=recovered)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def record_money(db: Session, *, category: str, amount_usd: float,
                 asset: str = "USD", tx_ref: str = "", verified: bool = False) -> LedgerEntry:
    if category not in {"revenue", "cost", "transfer"}:
        raise ValueError("invalid ledger category")
    if amount_usd < 0:
        raise ValueError("ledger amounts must be non-negative")
    row = LedgerEntry(category=category, amount_usd=amount_usd, asset=asset,
                      tx_ref=tx_ref, verified=verified)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
