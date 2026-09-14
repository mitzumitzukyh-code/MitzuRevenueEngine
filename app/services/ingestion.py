from sqlalchemy import select
from sqlalchemy.orm import Session
from app.adapters.base import DiscoveredOpportunity
from app.domain import Opportunity
from app.models import OpportunityRecord
from app.policy import decide
from app.scoring import score

def ingest(db: Session, item: DiscoveredOpportunity) -> tuple[OpportunityRecord, bool]:
    existing = db.scalar(select(OpportunityRecord).where(OpportunityRecord.external_id == item.external_id))
    if existing:
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
        success_probability=item.success_probability, decision=decision.value,
        status="discovered",
    )
    db.add(row); db.commit(); db.refresh(row)
    _ = score(op)
    return row, True
