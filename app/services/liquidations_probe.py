"""Read-only feasibility probe for public liquidation-market upstreams.

This module never trades, authenticates to an exchange account, signs requests,
or sends payments. It only checks public market-data endpoints.
"""
from dataclasses import asdict, dataclass
import time

import httpx


@dataclass(frozen=True)
class ProbeResult:
    source: str
    endpoint: str
    ok: bool
    latency_ms: int
    http_status: int
    auth_required: bool
    variable_source_cost_usd: float | None
    cost_status: str
    detail: str


async def _get(source: str, endpoint: str, params: dict) -> ProbeResult:
    started = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            response = await client.get(endpoint, params=params)
        latency = round((time.perf_counter() - started) * 1000)
        ok = response.status_code == 200
        return ProbeResult(
            source=source,
            endpoint=str(response.url),
            ok=ok,
            latency_ms=latency,
            http_status=response.status_code,
            auth_required=response.status_code in {401, 403},
            variable_source_cost_usd=0.0 if ok else None,
            cost_status="VERIFIED_PUBLIC_NO_PER_CALL_FEE" if ok else "UNVERIFIED",
            detail="Public market-data request succeeded." if ok else "Public request failed.",
        )
    except Exception as exc:
        return ProbeResult(
            source=source,
            endpoint=endpoint,
            ok=False,
            latency_ms=round((time.perf_counter() - started) * 1000),
            http_status=0,
            auth_required=False,
            variable_source_cost_usd=None,
            cost_status="UNVERIFIED",
            detail=type(exc).__name__,
        )


async def probe_liquidation_sources() -> list[dict]:
    checks = [
        ("binance_open_interest", "https://dapi.binance.com/dapi/v1/openInterest", {"symbol": "BTCUSD_PERP"}),
        ("bybit_open_interest", "https://api.bybit.com/v5/market/open-interest", {
            "category": "linear", "symbol": "BTCUSDT", "intervalTime": "5min", "limit": 1,
        }),
        ("okx_open_interest", "https://www.okx.com/api/v5/public/open-interest", {
            "instType": "SWAP", "instId": "BTC-USDT-SWAP",
        }),
        ("okx_mark_price", "https://www.okx.com/api/v5/public/mark-price", {
            "instType": "SWAP", "instId": "BTC-USDT-SWAP",
        }),
    ]
    results = []
    for source, endpoint, params in checks:
        results.append(asdict(await _get(source, endpoint, params)))
    return results
