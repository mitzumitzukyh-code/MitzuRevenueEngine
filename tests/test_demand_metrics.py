from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import MarketMetric, OpportunityRecord
from app.services.demand_metrics import rebuild_coinbase_category_metrics


def test_rebuild_replaces_stale_coinbase_metrics():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()

    db.add(MarketMetric(
        source="coinbase_bazaar",
        category="Exa",
        buyers_30d=281,
        transactions_30d=50714,
        volume_30d_usd=459.58,
    ))
    db.add(OpportunityRecord(
        source="coinbase_bazaar",
        external_id="coinbase:search",
        title="Search",
        category="search",
        calls_30d=100,
        unique_payers_30d=10,
        estimated_volume_30d_usd=1.0,
    ))
    db.commit()

    count = rebuild_coinbase_category_metrics(db)

    rows = db.scalars(
        select(MarketMetric).where(MarketMetric.source == "coinbase_bazaar")
    ).all()
    assert count == 1
    assert len(rows) == 1
    assert rows[0].category == "search"
    assert rows[0].buyers_30d == 10
    assert rows[0].transactions_30d == 100
