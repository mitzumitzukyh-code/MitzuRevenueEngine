from app.services.market_intelligence import research_priority

def _candidate(category, volume, calls, leader_calls, opportunity=63):
    return {
        "category": category,
        "signal": {
            "buyers_30d": 100,
            "transactions_30d": calls,
            "volume_30d_usd": volume,
            "competitors": 8,
        },
        "scores": {
            "demand": 61,
            "competition": 32,
            "opportunity": opportunity,
            "decision": "WATCH",
        },
        "flags": ["PROVEN_DEMAND"],
        "top_services": [{"calls_30d": leader_calls}],
        "reason": "test",
    }

def test_priority_exposes_unit_economics_metrics():
    ranked = research_priority(_candidate("liquidations", 36.264, 1900, 1393))
    metrics = ranked["research_metrics"]
    assert metrics["avg_revenue_per_call_usd"] == 0.019086
    assert metrics["leader_call_share"] == 0.7332
    assert ranked["next_action"] == "UNIT_ECONOMICS_RESEARCH"

def test_low_revenue_concentrated_market_is_penalized():
    strong = research_priority(_candidate("a", 100, 1000, 100))
    weak = research_priority(_candidate("b", 10, 1000, 900))
    assert strong["research_metrics"]["research_priority_score"] > weak["research_metrics"]["research_priority_score"]
