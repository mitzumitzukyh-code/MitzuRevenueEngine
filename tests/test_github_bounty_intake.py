from app.github_bounty_intake import bounty_amount, from_github_issue


def test_extracts_explicit_bounty_directive():
    assert bounty_amount("details\n/bounty $12") == 12
    assert bounty_amount("/BOUNTY $75.50") == 75.5


def test_ignores_issues_without_explicit_amount():
    assert bounty_amount("bounty maybe") is None


def test_normalizes_candidate_without_authorizing_it():
    job = from_github_issue(
        repo="tscircuit/file-server",
        number=5,
        title="download endpoint",
        body="/bounty $10",
        funded=True,
        success_probability=.8,
        estimated_ai_cost_usd=1,
    )
    assert job is not None
    assert job.payout_usd == 10
    assert job.source == "github:tscircuit/file-server#5"
