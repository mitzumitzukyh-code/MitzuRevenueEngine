from dataclasses import asdict

from sqlalchemy.orm import Session

from app.product_designer import ProductPlan
from app.sandbox_runtime import execute, health
from app.service_factory import build_blueprint
from app.services.product_opportunities import design_for_category


def _blueprint(db: Session, category: str):
    planned = design_for_category(db, category)
    if not planned:
        return None
    plan = ProductPlan(**planned["product"])
    return build_blueprint(plan)


def run_category(db: Session, category: str, payload: dict | None = None) -> dict | None:
    blueprint = _blueprint(db, category)
    if not blueprint:
        return None
    return asdict(execute(blueprint, payload))


def health_category(db: Session, category: str) -> dict | None:
    blueprint = _blueprint(db, category)
    return health(blueprint) if blueprint else None
