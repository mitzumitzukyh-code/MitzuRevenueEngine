from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.models import MarketMetric, OpportunityRecord
from app.services.market_intelligence import latest_signals


def test_latest_signals_counts_unique_source_provider_pairs():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    db.add(MarketMetric(source="x", category="liquidations", buyers_30d=3, transactions_30d=10, volume_30d_usd=2.0))
    common = dict(title="t", url="u", expected_revenue_usd=0, estimated_cost_usd=0, automation_score=0, payment_probability=0, success_probability=0, category="liquidations", network="", asset="", price_atomic="", pay_to="", calls_30d=0, unique_payers_30d=0, estimated_volume_30d_usd=0, decision="", status="")
    db.add(OpportunityRecord(source="bazaar", external_id="1", provider="same", **common))
    db.add(OpportunityRecord(source="bazaar", external_id="2", provider="same", **common))
    db.add(OpportunityRecord(source="open402", external_id="3", provider="same", **common))
    db.commit()
    signals = latest_signals(db, ["liquidations"])
    assert signals["liquidations"].competitors == 2
