"""Market snapshot normalization for Opportunity Scout.

Snapshots are evidence records, not permission to claim or bid.
"""
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class MarketSnapshot:
    source: str
    open_paid_jobs: int
    observed_at: str
    notes: str = ""


def snapshot(source: str, open_paid_jobs: int, notes: str = "") -> dict:
    if open_paid_jobs < 0:
        raise ValueError("open_paid_jobs must be non-negative")
    return {
        "source": source,
        "open_paid_jobs": open_paid_jobs,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "notes": notes,
        "action_authorized": False,
    }


def market_priority(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda row: row["open_paid_jobs"], reverse=True)
