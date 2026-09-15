from app.demand import MarketSignal, evaluate
from app.services.market_intelligence_service import classify_market

def test_dead_market_flag():
    signal = MarketSignal(0, 0, 0, 1)
    scored = evaluate(signal)
    assert "DEAD" in classify_market(signal, scored)

def test_saturated_market_flag():
    signal = MarketSignal(100, 5000, 5000, 40)
    scored = evaluate(signal)
    assert "SATURATED" in classify_market(signal, scored)

def test_proven_build_candidate_flags():
    signal = MarketSignal(100, 5000, 5000, 2)
    scored = evaluate(signal)
    flags = classify_market(signal, scored)
    assert "PROVEN_DEMAND" in flags
    assert "BUILD_CANDIDATE" in flags
