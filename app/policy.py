from app.config import settings
from app.domain import Decision, Opportunity

def decide(op: Opportunity) -> Decision:
    if op.automation_score < settings.min_automation_score:
        return Decision.REJECT
    if op.estimated_cost_usd > settings.max_task_cost_usd:
        return Decision.REJECT
    if op.expected_profit_usd < settings.min_expected_profit_usd:
        return Decision.REJECT
    if op.roi < settings.min_roi:
        return Decision.REJECT
    return Decision.EXECUTE if settings.autonomous_execution else Decision.REVIEW
