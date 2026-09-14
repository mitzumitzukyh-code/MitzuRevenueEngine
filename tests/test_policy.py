from app.domain import Decision, Opportunity
from app.policy import decide

def test_rejects_low_automation():
    op = Opportunity("test", "manual task", 100, 1, 50, 1, 1)
    assert decide(op) == Decision.REJECT

def test_safe_candidate_requires_review_by_default():
    op = Opportunity("test", "automatic api task", 20, 1, 100, 1, 1)
    assert decide(op) == Decision.REVIEW
