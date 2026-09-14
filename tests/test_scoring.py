from app.domain import Opportunity
from app.scoring import score

def test_score_is_bounded():
    op = Opportunity("x", "x", 1000, 0.01, 100, 1, 1)
    assert 0 <= score(op).value <= 100

def test_better_opportunity_scores_higher():
    weak = Opportunity("x", "weak", 2, 1, 90, .5, .5)
    strong = Opportunity("x", "strong", 20, 1, 100, 1, 1)
    assert score(strong).value > score(weak).value
