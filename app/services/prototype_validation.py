"""Repeated read-only validation for sandbox data products."""
from dataclasses import dataclass, asdict
import time

from app.services.liquidations_prototype import liquidation_snapshot


@dataclass(frozen=True)
class ValidationReport:
    product: str
    asset: str
    requested_runs: int
    successful_runs: int
    availability_pct: float
    avg_latency_ms: float
    p95_latency_ms: float
    source_cost_usd: float
    data_changed: bool
    verdict: str
    reason: str


async def validate_liquidations(asset: str, runs: int = 5) -> dict:
    runs = max(2, min(runs, 20))
    latencies = []
    snapshots = []
    failures = 0
    for _ in range(runs):
        started = time.perf_counter()
        try:
            value = await liquidation_snapshot(f"{asset}-USDT-SWAP")
            snapshots.append(value)
            latencies.append((time.perf_counter() - started) * 1000)
        except Exception:
            failures += 1
    successes = len(snapshots)
    availability = successes / runs * 100
    ordered = sorted(latencies)
    p95_index = max(0, min(len(ordered) - 1, int(len(ordered) * 0.95) - 1)) if ordered else 0
    p95 = ordered[p95_index] if ordered else 0.0
    marks = [x["mark_price"] for x in snapshots]
    changed = len(set(marks)) > 1
    total_source_cost = sum(float(x["source_cost_usd"]) for x in snapshots)

    if availability < 95:
        verdict, reason = "REJECT", "Upstream availability is below 95%."
    elif p95 > 2000:
        verdict, reason = "WATCH", "Availability passed but p95 latency is above 2 seconds."
    else:
        verdict, reason = "PASS", "Availability and latency gates passed in sandbox."

    return asdict(ValidationReport(
        product="liquidations",
        asset=asset,
        requested_runs=runs,
        successful_runs=successes,
        availability_pct=round(availability, 2),
        avg_latency_ms=round(sum(latencies) / len(latencies), 2) if latencies else 0.0,
        p95_latency_ms=round(p95, 2),
        source_cost_usd=round(total_source_cost, 6),
        data_changed=changed,
        verdict=verdict,
        reason=reason,
    ))
