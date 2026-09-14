from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.base import DiscoveredOpportunity
from app.db import Base
from app.services.ingestion import ingest

def test_existing_listing_refreshes_quality_metrics():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    first = DiscoveredOpportunity(
        source="coinbase_bazaar",
        external_id="same",
        title="service",
        calls_30d=2,
        unique_payers_30d=1,
    )
    row, created = ingest(db, first)
    assert created is True
    assert row.calls_30d == 2

    updated = DiscoveredOpportunity(
        source="coinbase_bazaar",
        external_id="same",
        title="service",
        calls_30d=50,
        unique_payers_30d=7,
        estimated_volume_30d_usd=1.25,
    )
    row2, created2 = ingest(db, updated)
    assert created2 is False
    assert row2.calls_30d == 50
    assert row2.unique_payers_30d == 7
    assert row2.estimated_volume_30d_usd == 1.25
