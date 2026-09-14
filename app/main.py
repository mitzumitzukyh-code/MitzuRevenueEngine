from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal, init_db
from app.models import ActivityEvent, LedgerEntry, MarketMetric, OpportunityRecord
from app.services.market_intelligence import build_candidate, classify_market, latest_signal, research_candidate, research_priority, score_category
from app.services.product_opportunities import design_for_category
from app.services.service_factory import blueprint_for_category
from app.services.sandbox_runtime import health_category, run_category
from app.services.evaluation_lab import evaluate_category
from app.services.deployment_planner import staging_plan

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


@app.get("/api/market/categories")
def market_categories(db: Session = Depends(get_db)):
    rows = db.execute(
        select(OpportunityRecord.category, func.count(OpportunityRecord.id))
        .where(OpportunityRecord.category != "")
        .group_by(OpportunityRecord.category)
        .order_by(func.count(OpportunityRecord.id).desc())
    ).all()
    return [{"category": category, "services": count} for category, count in rows]

@app.get("/api/market/networks")
def market_networks(db: Session = Depends(get_db)):
    rows = db.execute(
        select(OpportunityRecord.network, func.count(OpportunityRecord.id))
        .where(OpportunityRecord.network != "")
        .group_by(OpportunityRecord.network)
        .order_by(func.count(OpportunityRecord.id).desc())
    ).all()
    return [{"network": network, "services": count} for network, count in rows]

class MarketMetricIn(BaseModel):
    source: str
    category: str
    buyers_30d: int = 0
    transactions_30d: int = 0
    volume_30d_usd: float = 0

@app.post("/api/market/metrics")
def add_market_metric(payload: MarketMetricIn, db: Session = Depends(get_db)):
    row = MarketMetric(
        source=payload.source,
        category=payload.category,
        buyers_30d=max(payload.buyers_30d, 0),
        transactions_30d=max(payload.transactions_30d, 0),
        volume_30d_usd=max(payload.volume_30d_usd, 0),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "status": "stored"}

@app.get("/api/market/opportunities")
def market_opportunities(db: Session = Depends(get_db)):
    categories = db.scalars(
        select(OpportunityRecord.category)
        .where(OpportunityRecord.category != "")
        .distinct()
    ).all()
    result = []
    for category in categories:
        scored = score_category(db, category)
        if scored:
            result.append({
                "category": category,
                "demand_score": scored.demand,
                "competition_score": scored.competition,
                "opportunity_score": scored.opportunity,
                "decision": scored.decision,
                "flags": classify_market(latest_signal(db, category), scored),
            })
    return sorted(result, key=lambda x: x["opportunity_score"], reverse=True)


@app.get("/api/system/workers")
def worker_status(db: Session = Depends(get_db)):
    workers = ["scout", "market", "recovery"]
    result = []
    for worker in workers:
        last = db.scalars(
            select(ActivityEvent).where(ActivityEvent.worker == worker)
            .order_by(ActivityEvent.created_at.desc()).limit(1)
        ).first()
        result.append({
            "worker": worker,
            "last_seen": last.created_at if last else None,
            "last_message": last.message if last else "No activity yet",
            "last_was_error": last.is_error if last else False,
        })
    return result


@app.get("/api/market/build-candidates")
def market_build_candidates(db: Session = Depends(get_db)):
    categories = db.scalars(
        select(OpportunityRecord.category)
        .where(OpportunityRecord.category != "")
        .distinct()
    ).all()
    candidates = []
    for category in categories:
        candidate = build_candidate(db, category)
        if candidate:
            candidates.append(candidate)
    return sorted(
        candidates,
        key=lambda x: x["scores"]["opportunity"],
        reverse=True,
    )


@app.get("/api/products/plans")
def product_plans(db: Session = Depends(get_db)):
    categories = db.scalars(
        select(OpportunityRecord.category)
        .where(OpportunityRecord.category != "")
        .distinct()
    ).all()
    plans = []
    for category in categories:
        plan = design_for_category(db, category)
        if plan:
            plans.append(plan)
    return sorted(
        plans,
        key=lambda x: x["product"]["projected_monthly_profit_usd"],
        reverse=True,
    )


@app.get("/api/factory/blueprints")
def service_blueprints(db: Session = Depends(get_db)):
    categories = db.scalars(
        select(OpportunityRecord.category)
        .where(OpportunityRecord.category != "")
        .distinct()
    ).all()
    blueprints = []
    for category in categories:
        blueprint = blueprint_for_category(db, category)
        if blueprint:
            blueprints.append(blueprint)
    return blueprints


class SandboxRequest(BaseModel):
    payload: dict = {}


@app.get("/api/sandbox/{category}/health")
def sandbox_health(category: str, db: Session = Depends(get_db)):
    result = health_category(db, category)
    return result or {"status": "unavailable", "reason": "category is not a BUILD candidate"}


@app.post("/api/sandbox/{category}/run")
def sandbox_run(category: str, request: SandboxRequest, db: Session = Depends(get_db)):
    result = run_category(db, category, request.payload)
    return result or {
        "status": "blocked",
        "reason": "category is not a BUILD candidate",
        "payment_attempted": False,
    }


@app.post("/api/evaluation/{category}")
def evaluate_service(category: str, requests: int = 100, db: Session = Depends(get_db)):
    requests = max(1, min(requests, 1000))
    result = evaluate_category(db, category, requests)
    return result or {
        "verdict": "BLOCKED",
        "reason": "category is not a BUILD candidate",
        "production_deploy": False,
    }


@app.get("/api/deployment/staging/{category}")
def deployment_staging_plan(category: str, requests: int = 100, db: Session = Depends(get_db)):
    result = staging_plan(db, category, max(1, min(requests, 1000)))
    return result or {
        "staging_eligible": False,
        "deployment_blocked": True,
        "block_reason": "NO_VALID_BUILD_CANDIDATE",
    }


@app.get("/api/market/research-candidates")
def market_research_candidates(db: Session = Depends(get_db)):
    categories = db.scalars(
        select(OpportunityRecord.category)
        .where(OpportunityRecord.category != "")
        .distinct()
    ).all()
    candidates = []
    for category in categories:
        candidate = research_candidate(db, category)
        if candidate:
            candidates.append(research_priority(candidate))
    return sorted(
        candidates,
        key=lambda x: x["research_metrics"]["research_priority_score"],
        reverse=True,
    )
