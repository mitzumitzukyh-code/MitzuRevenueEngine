from app.payment_offer_preview import preview_payment_offer


def test_preview_never_advertises_or_settles():
    result = preview_payment_offer("0x" + "1" * 40)
    assert result["mode"] == "PREVIEW_ONLY"
    assert result["advertised_to_clients"] is False
    assert result["settlement_enabled"] is False
    assert result["offer"]["network"] == "eip155:84532"
    assert result["offer"]["scheme"] == "exact"
    assert result["offer"]["amount"] == "5000"
    assert result["offer"]["asset"] is None
    assert "testnet_asset_contract_not_verified" in result["blockers"]


def test_invalid_receiver_is_not_inserted():
    result = preview_payment_offer("bad")
    assert result["offer"]["payTo"] is None
    assert "receiver_wallet_not_configured_or_invalid" in result["blockers"]
