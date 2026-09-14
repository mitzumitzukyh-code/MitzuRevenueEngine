from sqlalchemy.orm import Session

from app.product_designer import ProductPlan
from app.service_factory import blueprint_dict
from app.services.product_opportunities import design_for_category


def blueprint_for_category(db: Session, category: str) -> dict | None:
    planned = design_for_category(db, category)
    if not planned:
        return None
    product = planned["product"]
    plan = ProductPlan(**product)
    return {
        "category": category,
        "product": product,
        "blueprint": blueprint_dict(plan),
        "factory_status": "SANDBOX_READY",
        "deploy_status": "BLOCKED",
        "wallet_status": "NOT_REQUIRED",
    }
