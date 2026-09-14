from sqlalchemy import select
from sqlalchemy.orm import Session
from app.adapters.base import DiscoveredOpportunity
from app.domain import Opportunity
from app.models import OpportunityRecord
from app.policy import decide

def ingest(db: Session, item: DiscoveredOpportunity) -> tuple[OpportunityRecord, bool]:
    existing = db.scalar(select(OpportunityRecord).where(OpportunityRecord.external_id == item.external_id))
    if existing:
        existing.title = item.title
        existing.url = item.url
        existing.category = item.category
        existing.provider = item.provider
        existing.network = item.network
        existing.asset = item.asset
        existing.price_atomic = item.price_atomic
        existing.pay_to = item.pay_to
        existing.calls_30d = item.calls_30d
        existing.unique_payers_30d = item.unique_payers_30d
        existing.estimated_volume_30d_usd = item.estimated_volume_30d_usd
        db.commit()
        db.refresh(existing)
        return existing, False
    op = Opportunity(
        source=item.source, title=item.title,
        expected_revenue_usd=item.expected_revenue_usd,
        estimated_cost_usd=item.estimated_cost_usd,
        automation_score=item.automation_score,
        payment_probability=item.payment_probability,
        success_probability=item.success_probability,
    )
    decision = decide(op)
    row = OpportunityRecord(
        source=item.source, external_id=item.external_id, title=item.title, url=item.url,
        expected_revenue_usd=item.expected_revenue_usd, estimated_cost_usd=item.estimated_cost_usd,
        automation_score=item.automation_score, payment_probability=item.payment_probability,
        success_probability=item.success_probability,
        category=item.category, provider=item.provider, network=item.network,
        asset=item.asset, price_atomic=item.price_atomic, pay_to=item.pay_to,
        calls_30d=item.calls_30d, unique_payers_30d=item.unique_payers_30d,
        estimated_volume_30d_usd=item.estimated_volume_30d_usd,
        decision=decision.value,
        status="discovered",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row, True
