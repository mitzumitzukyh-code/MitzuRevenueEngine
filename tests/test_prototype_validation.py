import asyncio

from app.services import prototype_validation


def test_validation_passes_stable_zero_cost_upstream(monkeypatch):
    counter = {"n": 0}

    async def fake_snapshot(symbol):
        counter["n"] += 1
        return {"mark_price": 100 + counter["n"], "source_cost_usd": 0.0}

    monkeypatch.setattr(prototype_validation, "liquidation_snapshot", fake_snapshot)
    result = asyncio.run(prototype_validation.validate_liquidations("BTC", 5))
    assert result["successful_runs"] == 5
    assert result["availability_pct"] == 100.0
    assert result["source_cost_usd"] == 0.0
    assert result["data_changed"] is True
    assert result["verdict"] == "PASS"


def test_validation_rejects_unavailable_upstream(monkeypatch):
    async def fail(symbol):
        raise RuntimeError("down")

    monkeypatch.setattr(prototype_validation, "liquidation_snapshot", fail)
    result = asyncio.run(prototype_validation.validate_liquidations("BTC", 5))
    assert result["availability_pct"] == 0.0
    assert result["verdict"] == "REJECT"
