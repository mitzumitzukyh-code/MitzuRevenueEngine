from app.break_even import calculate_break_even


def test_break_even_and_first_dollar():
    result = calculate_break_even(
        price_per_call_usd=0.019,
        variable_cost_per_call_usd=0.0,
        fixed_cost_per_month_usd=5.0,
    )
    assert result["calls_to_break_even"] == 264
    assert result["calls_for_first_dollar_profit"] == 316


def test_non_positive_contribution_never_breaks_even():
    result = calculate_break_even(
        price_per_call_usd=0.01,
        variable_cost_per_call_usd=0.01,
        fixed_cost_per_month_usd=5.0,
    )
    assert result["calls_to_break_even"] is None
