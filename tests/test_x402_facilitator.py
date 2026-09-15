from app.x402_facilitator import (
    build_settle_payload,
    build_verify_payload,
    facilitator_plan,
)


def test_facilitator_is_testnet_and_fail_closed():
    plan = facilitator_plan()
    assert plan["network"] == "eip155:84532"
    assert plan["testnet_only"] is True
    assert plan["verify_enabled"] is False
    assert plan["settle_enabled"] is False
    assert plan["real_funds"] is False


def test_verify_and_settle_payload_shapes_match_protocol():
    payment = {"x402Version": 2, "payload": {"signature": "test-only"}}
    requirements = {"scheme": "exact", "network": "eip155:84532"}
    expected = {
        "paymentPayload": payment,
        "paymentRequirements": requirements,
    }
    assert build_verify_payload(payment, requirements) == expected
    assert build_settle_payload(payment, requirements) == expected
