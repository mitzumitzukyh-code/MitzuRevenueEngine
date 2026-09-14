from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.base import DiscoveredOpportunity
from app.db import Base
from app.services.ingestion import ingest

def test_ingestion_deduplicates_external_id():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    item = DiscoveredOpportunity("x402", "same-id", "service")
    first, created1 = ingest(db, item)
    second, created2 = ingest(db, item)
    assert created1 is True
    assert created2 is False
    assert first.id == second.id
