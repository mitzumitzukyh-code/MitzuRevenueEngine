"""Read-only liquidation-cluster prototype using public OKX market data.

This is a heuristic market-data product, not an exchange liquidation feed and
not trading advice. It does not place orders, authenticate, sign, or pay.
"""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

import httpx


@dataclass(frozen=True)
class LiquidationCluster:
    leverage: int
    long_liq_estimate: float
    short_liq_estimate: float


@dataclass(frozen=True)
class LiquidationSnapshot:
    symbol: str
    mark_price: float
    open_interest: float
    clusters: list[LiquidationCluster]
    methodology: str
    source: str
    source_cost_usd: float
    generated_at: str


async def _okx_json(path: str, params: dict) -> dict:
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get("https://www.okx.com" + path, params=params)
        response.raise_for_status()
        payload = response.json()
    if payload.get("code") != "0" or not payload.get("data"):
        raise RuntimeError("OKX public market-data response was not usable")
    return payload["data"][0]


async def liquidation_snapshot(symbol: str = "BTC-USDT-SWAP") -> dict:
    mark = await _okx_json(
        "/api/v5/public/mark-price",
        {"instType": "SWAP", "instId": symbol},
    )
    oi = await _okx_json(
        "/api/v5/public/open-interest",
        {"instType": "SWAP", "instId": symbol},
    )
    mark_price = float(mark["markPx"])
    open_interest = float(oi["oi"])

    clusters = []
    for leverage in (5, 10, 25, 50):
        distance = 1 / leverage
        clusters.append(LiquidationCluster(
            leverage=leverage,
            long_liq_estimate=round(mark_price * (1 - distance), 2),
            short_liq_estimate=round(mark_price * (1 + distance), 2),
        ))

    snapshot = LiquidationSnapshot(
        symbol=symbol,
        mark_price=mark_price,
        open_interest=open_interest,
        clusters=clusters,
        methodology=(
            "Heuristic leverage-band estimates from public OKX mark price. "
            "These are not observed liquidation orders or predicted exact liquidation prices."
        ),
        source="OKX public mark price + open interest",
        source_cost_usd=0.0,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
    return {
        **asdict(snapshot),
        "read_only": True,
        "trading": False,
        "payments": False,
        "financial_advice": False,
    }
