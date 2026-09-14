from app.demand import MarketSignal
from app.unit_economics import assess_unit_economics


SIGNAL = MarketSignal(
    buyers_30d=129,
    transactions_30d=1900,
    volume_30d_usd=36.264,
    competitors=8,
)


def test_unverified_cost_cannot_promote():
    result = assess_unit_economics(
        category="liquidations",
        signal=SIGNAL,
        estimated_variable_cost_per_call_usd=0,
        source_cost_status="UNVERIFIED",
    )
    assert result.verdict == "RESEARCH"


def test_verified_zero_variable_cost_can_promote_to_prototype():
    result = assess_unit_economics(
        category="liquidations",
        signal=SIGNAL,
        estimated_variable_cost_per_call_usd=0,
        source_cost_status="VERIFIED",
    )
    assert result.verdict == "PROTOTYPE"
    assert result.gross_margin_pct == 100.0


def test_verified_expensive_source_is_rejected():
    result = assess_unit_economics(
        category="liquidations",
        signal=SIGNAL,
        estimated_variable_cost_per_call_usd=0.03,
        source_cost_status="VERIFIED",
    )
    assert result.verdict == "REJECT"
