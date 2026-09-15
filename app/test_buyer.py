"""Test-buyer safety blueprint for x402 v2 on Base Sepolia.

No private key is generated or stored here. Signing is intentionally absent
until an isolated test payer wallet is provisioned.
"""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TestBuyerPlan:
    network: str = "eip155:84532"
    scheme: str = "exact"
    asset_transfer_method: str = "eip3009"
    payer_wallet_configured: bool = False
    signing_enabled: bool = False
    verify_enabled: bool = True
    settle_enabled: bool = False
    real_funds: bool = False
    receiver_separate_from_payer: bool = True


def test_buyer_plan() -> dict:
    return asdict(TestBuyerPlan())


def required_authorization_fields() -> tuple[str, ...]:
    return ("from", "to", "value", "validAfter", "validBefore", "nonce")


def payment_signature_ready(payload: dict) -> bool:
    authorization = payload.get("authorization")
    signature = payload.get("signature")
    return bool(
        isinstance(signature, str)
        and signature.startswith("0x")
        and isinstance(authorization, dict)
        and all(field in authorization for field in required_authorization_fields())
    )
