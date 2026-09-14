import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.ledger import record_event, record_money

@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()

def test_activity_event_is_persisted(db):
    row = record_event(db, kind="scan", worker="scout", message="scan complete")
    assert row.id is not None
    assert row.is_error is False

def test_money_requires_valid_category(db):
    with pytest.raises(ValueError):
        record_money(db, category="magic", amount_usd=10)

def test_money_rejects_negative_amount(db):
    with pytest.raises(ValueError):
        record_money(db, category="revenue", amount_usd=-1)
