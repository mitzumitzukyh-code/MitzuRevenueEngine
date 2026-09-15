from app.pricing_validation import validate_liquidations_pricing


def test_pricing_range_and_hypothesis_are_conservative():
    result = validate_liquidations_pricing()
    assert result["comparable_count"] == 3
    assert result["min_price_usd"] == 0.005
    assert result["median_price_usd"] == 0.01
    assert result["max_price_usd"] == 0.10
    assert result["recommended_entry_price_usd"] == 0.005
    assert result["verdict"] == "PRICE_HYPOTHESIS"
