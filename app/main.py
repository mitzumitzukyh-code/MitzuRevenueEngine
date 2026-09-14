from fastapi import FastAPI
from app.config import settings

app = FastAPI(title="Mitzu Revenue Engine", version="0.1.0")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.app_env,
        "autonomous_execution": settings.autonomous_execution,
        "wallet_enabled": settings.wallet_enabled,
    }

@app.get("/api/dashboard/summary")
def dashboard_summary():
    return {
        "status": "ONLINE",
        "revenue_today_usd": 0,
        "cost_today_usd": 0,
        "net_profit_today_usd": 0,
        "opportunities_seen": 0,
        "executed": 0,
        "successful": 0,
        "failed": 0,
    }
