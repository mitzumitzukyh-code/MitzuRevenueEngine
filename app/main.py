from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal, init_db
from app.models import ActivityEvent, LedgerEntry, OpportunityRecord

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Mitzu Revenue Engine", version="0.1.0", lifespan=lifespan)

@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse("web/index.html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.app_env,
        "autonomous_execution": settings.autonomous_execution,
        "wallet_enabled": settings.wallet_enabled,
    }

@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).date()
    ledger = db.scalars(select(LedgerEntry)).all()
    revenue = sum(x.amount_usd for x in ledger if x.category == "revenue" and x.created_at.date() == today and x.verified)
    costs = sum(x.amount_usd for x in ledger if x.category == "cost" and x.created_at.date() == today)
    opportunities = db.scalar(select(func.count()).select_from(OpportunityRecord)) or 0
    executed = db.scalar(select(func.count()).select_from(OpportunityRecord).where(OpportunityRecord.status == "executed")) or 0
    successful = db.scalar(select(func.count()).select_from(OpportunityRecord).where(OpportunityRecord.status == "successful")) or 0
    failed = db.scalar(select(func.count()).select_from(OpportunityRecord).where(OpportunityRecord.status == "failed")) or 0
    return {
        "status": "ONLINE",
        "revenue_today_usd": round(revenue, 4),
        "cost_today_usd": round(costs, 4),
        "net_profit_today_usd": round(revenue - costs, 4),
        "opportunities_seen": opportunities,
        "executed": executed,
        "successful": successful,
        "failed": failed,
    }

@app.get("/api/activity")
def activity(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 200))
    rows = db.scalars(select(ActivityEvent).order_by(ActivityEvent.created_at.desc()).limit(limit)).all()
    return [{"id": x.id, "kind": x.kind, "worker": x.worker, "message": x.message,
             "amount_usd": x.amount_usd, "is_error": x.is_error,
             "recovered": x.recovered, "created_at": x.created_at} for x in rows]

@app.get("/api/errors")
def errors(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 200))
    rows = db.scalars(select(ActivityEvent).where(ActivityEvent.is_error.is_(True))
                      .order_by(ActivityEvent.created_at.desc()).limit(limit)).all()
    return [{"id": x.id, "worker": x.worker, "message": x.message,
             "recovered": x.recovered, "created_at": x.created_at} for x in rows]
