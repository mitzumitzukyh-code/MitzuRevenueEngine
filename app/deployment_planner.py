from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DeploymentPlan:
    service_id: str
    environment: str
    replicas: int
    healthcheck_path: str
    healthcheck_interval_seconds: int
    restart_policy: str
    rollback_enabled: bool
    monthly_budget_cap_usd: float
    wallet_enabled: bool
    x402_enabled: bool
    deploy_allowed: bool
    required_gates: tuple[str, ...]


def plan_staging(service_id: str, healthcheck_path: str) -> DeploymentPlan:
    return DeploymentPlan(
        service_id=service_id,
        environment="staging",
        replicas=1,
        healthcheck_path=healthcheck_path,
        healthcheck_interval_seconds=60,
        restart_policy="unless-stopped",
        rollback_enabled=True,
        monthly_budget_cap_usd=0.0,
        wallet_enabled=False,
        x402_enabled=False,
        deploy_allowed=False,
        required_gates=(
            "CI_GREEN",
            "EVALUATION_PASS",
            "ZERO_PAYMENT_ATTEMPTS",
            "ZERO_EXTERNAL_SPEND",
            "EXPLICIT_DEPLOY_APPROVAL",
        ),
    )


def plan_dict(service_id: str, healthcheck_path: str) -> dict:
    return asdict(plan_staging(service_id, healthcheck_path))
