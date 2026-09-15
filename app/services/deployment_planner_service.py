from sqlalchemy.orm import Session

from app.deployment_planner import plan_dict
from app.services.evaluation_service import evaluate_category
from app.services.service_factory_service import blueprint_for_category


def staging_plan(db: Session, category: str, requests: int = 100) -> dict | None:
    evaluation = evaluate_category(db, category, requests)
    blueprint = blueprint_for_category(db, category)
    if not evaluation or not blueprint:
        return None
    service = blueprint["blueprint"]
    plan = plan_dict(service["service_id"], service["health_route"])
    return {
        "category": category,
        "evaluation": evaluation,
        "deployment": plan,
        "staging_eligible": evaluation["verdict"] == "PASS",
        "deployment_blocked": True,
        "block_reason": "EXPLICIT_DEPLOY_APPROVAL_REQUIRED",
    }
