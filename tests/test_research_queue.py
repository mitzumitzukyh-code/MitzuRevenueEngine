from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import MarketMetric, OpportunityRecord
from app.services.market_intelligence_service import research_candidate


def test_research_candidate_requires_proven_non_saturated_watch_market():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()

    db.add(MarketMetric(
        source="coinbase_bazaar",
        category="content",
        buyers_30d=20,
        transactions_30d=500,
        volume_30d_usd=500,
    ))
    for i in range(3):
        db.add(OpportunityRecord(
            source="coinbase_bazaar",
            external_id=f"content-{i}",
            title=f"Content {i}",
            provider="provider",
            category="content",
            calls_30d=100 - i,
            unique_payers_30d=10,
            estimated_volume_30d_usd=10,
            url=f"https://example.com/{i}",
        ))
    db.commit()

    candidate = research_candidate(db, "content")
    assert candidate is not None
    assert candidate["scores"]["decision"] == "WATCH"
    assert "PROVEN_DEMAND" in candidate["flags"]
    assert "SATURATED" not in candidate["flags"]
    assert len(candidate["top_services"]) == 3
