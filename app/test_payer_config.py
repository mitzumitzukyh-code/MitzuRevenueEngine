"""Environment guard for an isolated Base Sepolia payer.

The payer secret is intentionally never returned, logged, or accepted as a
production wallet credential.
"""
import os

from app.payment_readiness import EVM_ADDRESS

DEFAULT_TEST_PAYER_ADDRESS = "0x15Dac2652358377Cc5e855a0f1F86B3C44A45E6f"


def test_payer_status() -> dict:
    address = os.getenv("X402_TEST_PAYER_ADDRESS", DEFAULT_TEST_PAYER_ADDRESS).strip()
    key_present = bool(os.getenv("X402_TEST_PAYER_PRIVATE_KEY", "").strip())
    valid = bool(address and EVM_ADDRESS.fullmatch(address))
    return {
        "address": address if valid else None,
        "address_valid": valid,
        "private_key_present": key_present,
        "private_key_exposed": False,
        "network": "eip155:84532",
        "testnet_only": True,
        "signing_enabled": valid and key_present,
        "settlement_enabled": False,
        "real_funds": False,
        "blockers": [
            *([] if valid else ["test_payer_address_missing_or_invalid"]),
            *([] if key_present else ["test_payer_key_missing"]),
            "settlement_disabled",
        ],
    }
