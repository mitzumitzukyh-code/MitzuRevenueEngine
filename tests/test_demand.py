from app.demand import MarketSignal, evaluate

def test_dead_market_is_rejected():
    s = evaluate(MarketSignal(0, 0, 0, 1))
    assert s.decision == "REJECT"

def test_active_low_competition_market_can_build():
    s = evaluate(MarketSignal(80, 5000, 5000, 2))
    assert s.decision == "BUILD"
    assert s.opportunity >= 80

def test_busy_market_with_heavy_competition_is_not_overrated():
    low = evaluate(MarketSignal(50, 1000, 1000, 50))
    high = evaluate(MarketSignal(50, 1000, 1000, 2))
    assert high.opportunity > low.opportunity
