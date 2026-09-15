from app.receiver_config import receiver_status


def test_missing_receiver_is_blocked(monkeypatch):
    monkeypatch.delenv("X402_RECEIVER_ADDRESS", raising=False)
    result = receiver_status()
    assert result["configured"] is False
    assert result["private_key_required"] is False
    assert result["settlement_enabled"] is False


def test_public_receiver_never_requires_private_key(monkeypatch):
    monkeypatch.setenv("X402_RECEIVER_ADDRESS", "0x" + "1" * 40)
    result = receiver_status()
    assert result["valid"] is True
    assert result["receive_only"] is True
    assert result["private_key_present"] is False
    assert result["blockers"] == ["settlement_disabled"]
