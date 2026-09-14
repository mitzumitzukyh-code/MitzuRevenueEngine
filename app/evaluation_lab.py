from dataclasses import asdict, dataclass
from statistics import mean

from app.sandbox_runtime import execute
from app.service_factory import ServiceBlueprint


@dataclass(frozen=True)
class EvaluationReport:
    service_id: str
    requests: int
    successes: int
    failures: int
    success_rate_pct: float
    avg_latency_ms: float
    max_latency_ms: float
    total_estimated_cost_usd: float
    payment_attempts: int
    verdict: str


def evaluate_blueprint(blueprint: ServiceBlueprint, requests: int = 100) -> EvaluationReport:
    count = max(1, min(requests, 1000))
    results = [execute(blueprint, {"evaluation_request": i}) for i in range(count)]
    successes = sum(r.status == "ok" for r in results)
    failures = count - successes
    latencies = [r.latency_ms for r in results]
    costs = sum(r.estimated_cost_usd for r in results)
    payments = sum(r.payment_attempted for r in results)
    success_rate = round(successes / count * 100, 2)
    avg_latency = round(mean(latencies), 3)
    max_latency = round(max(latencies), 3)
    verdict = "PASS" if success_rate >= 99 and payments == 0 and costs == 0 else "FAIL"
    return EvaluationReport(
        service_id=blueprint.service_id,
        requests=count,
        successes=successes,
        failures=failures,
        success_rate_pct=success_rate,
        avg_latency_ms=avg_latency,
        max_latency_ms=max_latency,
        total_estimated_cost_usd=round(costs, 6),
        payment_attempts=payments,
        verdict=verdict,
    )


def report_dict(blueprint: ServiceBlueprint, requests: int = 100) -> dict:
    return asdict(evaluate_blueprint(blueprint, requests))
