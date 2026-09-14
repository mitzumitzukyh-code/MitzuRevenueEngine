from app.deployment_planner import plan_staging


def test_staging_plan_is_zero_budget_and_blocked():
    plan = plan_staging("mitzu-data-api", "/services/mitzu-data-api/health")
    assert plan.environment == "staging"
    assert plan.monthly_budget_cap_usd == 0
    assert plan.wallet_enabled is False
    assert plan.x402_enabled is False
    assert plan.deploy_allowed is False


def test_staging_plan_requires_rollback_and_approval():
    plan = plan_staging("mitzu-data-api", "/health")
    assert plan.rollback_enabled is True
    assert "EXPLICIT_DEPLOY_APPROVAL" in plan.required_gates
