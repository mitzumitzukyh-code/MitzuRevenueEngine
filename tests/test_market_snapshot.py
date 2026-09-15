import pytest
from app.market_snapshot import market_priority, snapshot


def test_snapshot_never_authorizes_external_action():
    row = snapshot("example", 3)
    assert row["action_authorized"] is False
    assert row["open_paid_jobs"] == 3


def test_priority_prefers_observed_paid_supply():
    rows = [snapshot("empty", 0), snapshot("live", 1)]
    assert [x["source"] for x in market_priority(rows)] == ["live", "empty"]


def test_negative_supply_is_rejected():
    with pytest.raises(ValueError):
        snapshot("bad", -1)
