"""Fail-closed x402 facilitator client for Base Sepolia.

This adapter only prepares verification/settlement requests. Network execution
is disabled by default and must be explicitly enabled in a later testnet-only
change.
"""
from dataclasses import asdict, dataclass

FACILITATOR_URL = "https://x402.org/facilitator"


@dataclass(frozen=True)
class FacilitatorPlan:
    facilitator_url: str
    network: str
    testnet_only: bool
    verify_enabled: bool
    settle_enabled: bool
    real_funds: bool


def facilitator_plan() -> dict:
    return asdict(FacilitatorPlan(
        facilitator_url=FACILITATOR_URL,
        network="eip155:84532",
        testnet_only=True,
        verify_enabled=True,
        settle_enabled=False,
        real_funds=False,
    ))


def build_verify_payload(payment_payload: dict, payment_requirements: dict) -> dict:
    return {
        "paymentPayload": payment_payload,
        "paymentRequirements": payment_requirements,
    }


def build_settle_payload(payment_payload: dict, payment_requirements: dict) -> dict:
    return build_verify_payload(payment_payload, payment_requirements)


def verify_endpoint() -> str:
    return f"{FACILITATOR_URL}/verify"


def malformed_probe_payload(payment_requirements: dict) -> dict:
    """Intentionally invalid payload for read-only facilitator smoke tests."""
    return {
        "x402Version": 2,
        "paymentPayload": {
            "x402Version": 2,
            "accepted": payment_requirements,
            "payload": {},
        },
        "paymentRequirements": payment_requirements,
    }
