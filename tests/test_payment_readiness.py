from app.payment_readiness import payment_readiness


def test_no_receiver_keeps_payment_blocked():
    result = payment_readiness()
    assert result["network"] == "eip155:84532"
    assert result["settlement_enabled"] is False
    assert result["real_funds"] is False
    assert "receiver_wallet_not_configured" in result["blockers"]


def test_valid_receiver_still_cannot_settle():
    result = payment_readiness("0x" + "1" * 40)
    assert result["receiver_valid"] is True
    assert result["settlement_enabled"] is False
    assert result["blockers"] == ["settlement_disabled"]


def test_invalid_receiver_is_rejected():
    result = payment_readiness("not-a-wallet")
    assert result["receiver_valid"] is False
    assert "receiver_wallet_invalid" in result["blockers"]
