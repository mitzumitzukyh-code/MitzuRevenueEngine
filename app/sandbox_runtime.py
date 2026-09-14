from dataclasses import dataclass
from time import perf_counter

from app.service_factory import ServiceBlueprint


@dataclass(frozen=True)
class SandboxResult:
    service_id: str
    status: str
    latency_ms: float
    estimated_cost_usd: float
    billable: bool
    payment_attempted: bool
    response: dict


def execute(blueprint: ServiceBlueprint, payload: dict | None = None) -> SandboxResult:
    start = perf_counter()
    payload = payload or {}
    response = {
        "service": blueprint.product_name,
        "category": blueprint.category,
        "mode": "sandbox",
        "received": payload,
        "result": {
            "status": "simulated",
            "message": "Sandbox execution completed without external spend.",
        },
    }
    latency_ms = round((perf_counter() - start) * 1000, 3)
    return SandboxResult(
        service_id=blueprint.service_id,
        status="ok",
        latency_ms=latency_ms,
        estimated_cost_usd=0.0,
        billable=False,
        payment_attempted=False,
        response=response,
    )


def health(blueprint: ServiceBlueprint) -> dict:
    return {
        "service_id": blueprint.service_id,
        "status": "healthy",
        "mode": "sandbox",
        "x402_enabled": False,
        "wallet_required": False,
        "spending_allowed": False,
    }
