import pytest
from app.services.liquidations_probe import ProbeResult

def test_probe_result_explicitly_tracks_cost_verification():
    result = ProbeResult(
        source="test",
        endpoint="https://example.com",
        ok=True,
        latency_ms=10,
        http_status=200,
        auth_required=False,
        variable_source_cost_usd=0.0,
        cost_status="VERIFIED_PUBLIC_NO_PER_CALL_FEE",
        detail="Public market-data request succeeded.",
    )
    assert result.auth_required is False
    assert result.variable_source_cost_usd == 0.0
    assert result.cost_status.startswith("VERIFIED")
