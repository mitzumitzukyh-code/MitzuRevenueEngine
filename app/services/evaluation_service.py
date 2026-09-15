from sqlalchemy.orm import Session

from app.evaluation_lab import report_dict
from app.product_designer import ProductPlan
from app.service_factory import build_blueprint
from app.services.product_opportunities_service import design_for_category


def evaluate_category(db: Session, category: str, requests: int = 100) -> dict | None:
    planned = design_for_category(db, category)
    if not planned:
        return None
    blueprint = build_blueprint(ProductPlan(**planned["product"]))
    report = report_dict(blueprint, requests)
    report["category"] = category
    report["promotion_status"] = "ELIGIBLE_FOR_STAGING" if report["verdict"] == "PASS" else "BLOCKED"
    report["production_deploy"] = False
    return report
