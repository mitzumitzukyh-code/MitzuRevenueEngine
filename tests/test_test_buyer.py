from app.test_buyer import (
    payment_signature_ready,
    required_authorization_fields,
    test_buyer_plan,
)


def test_buyer_starts_without_signing_or_settlement():
    plan = test_buyer_plan()
    assert plan["network"] == "eip155:84532"
    assert plan["asset_transfer_method"] == "eip3009"
    assert plan["payer_wallet_configured"] is False
    assert plan["signing_enabled"] is False
    assert plan["settle_enabled"] is False
    assert plan["real_funds"] is False
    assert plan["receiver_separate_from_payer"] is True


def test_signature_requires_complete_eip3009_authorization():
    assert required_authorization_fields() == (
        "from", "to", "value", "validAfter", "validBefore", "nonce"
    )
    assert payment_signature_ready({}) is False
