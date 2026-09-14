from dataclasses import asdict, dataclass
import re

from app.product_designer import ProductPlan


@dataclass(frozen=True)
class ServiceBlueprint:
    service_id: str
    product_name: str
    category: str
    route: str
    health_route: str
    unit_price_usd: float
    payment_protocol: str
    settlement_asset: str
    sandbox_only: bool
    autonomous_deploy: bool
    manifest: dict


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "service"


def build_blueprint(plan: ProductPlan) -> ServiceBlueprint:
    slug = _slug(plan.product_name)
    route = f"/services/{slug}"
    manifest = {
        "name": plan.product_name,
        "category": plan.category,
        "endpoint": route,
        "health": f"{route}/health",
        "pricing": {
            "amount_usd": plan.unit_price_usd,
            "model": "per_call",
        },
        "x402": {
            "enabled": False,
            "protocol": "x402",
            "asset": "USDC",
            "network": "UNCONFIGURED",
            "pay_to": "UNCONFIGURED",
        },
        "safety": {
            "sandbox_only": True,
            "wallet_required": False,
            "spending_allowed": False,
        },
    }
    return ServiceBlueprint(
        service_id=slug,
        product_name=plan.product_name,
        category=plan.category,
        route=route,
        health_route=f"{route}/health",
        unit_price_usd=plan.unit_price_usd,
        payment_protocol="x402",
        settlement_asset="USDC",
        sandbox_only=True,
        autonomous_deploy=False,
        manifest=manifest,
    )


def blueprint_dict(plan: ProductPlan) -> dict:
    return asdict(build_blueprint(plan))
