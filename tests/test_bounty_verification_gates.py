from app.opportunity_scout import BountyOpportunity, eligible


def base(**overrides):
    values = dict(source="x", title="job", payout_usd=50, funded=True,
                  verified_funding_usd=50, success_probability=.8,
                  repo_active=True, payout_terms_clear=True)
    values.update(overrides)
    return BountyOpportunity(**values)


def test_verified_low_competition_bounty_is_eligible():
    assert eligible(base(competing_claims=2))


def test_unverified_funding_is_rejected():
    assert not eligible(base(verified_funding_usd=0))


def test_overcommitted_bounty_is_rejected():
    assert not eligible(base(competing_claims=12))


def test_secret_exfiltration_requirement_is_rejected():
    assert not eligible(base(secret_exfiltration_risk=True))


def test_inactive_repo_or_unclear_payout_is_rejected():
    assert not eligible(base(repo_active=False))
    assert not eligible(base(payout_terms_clear=False))
