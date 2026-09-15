from app.opportunity_scout import BountyOpportunity, SAFETY_POLICY, eligible, rank


def test_rejects_unfunded_or_capital_required_work():
    assert not eligible(BountyOpportunity("x", "unfunded", 25, False, success_probability=.9))
    assert not eligible(BountyOpportunity("x", "deposit", 25, True, 1, .9, requires_deposit=True))


def test_rejects_spam_trading_and_low_probability():
    assert not eligible(BountyOpportunity("x", "spam", 25, True, success_probability=.9, requires_spam=True))
    assert not eligible(BountyOpportunity("x", "trade", 25, True, success_probability=.9, requires_trading=True))
    assert not eligible(BountyOpportunity("x", "hard", 25, True, success_probability=.69))


def test_ranks_by_expected_value():
    jobs = [
        BountyOpportunity("a", "small", 10, True, success_probability=.9, estimated_ai_cost_usd=1),
        BountyOpportunity("b", "better", 20, True, success_probability=.8, estimated_ai_cost_usd=2),
    ]
    assert [x["title"] for x in rank(jobs)] == ["better", "small"]


def test_money_and_signing_stay_human_gated():
    assert SAFETY_POLICY["may_discover"] is True
    assert SAFETY_POLICY["may_prepare_work"] is True
    assert SAFETY_POLICY["may_accept_external_commitment"] is False
    assert SAFETY_POLICY["may_spend"] is False
    assert SAFETY_POLICY["may_sign_transaction"] is False
    assert SAFETY_POLICY["may_expose_wallet_secret"] is False
