"""Receive-only public-address configuration.

The application may know a public receiver address, but never stores or needs
a private key. Settlement remains separately gated.
"""
import os
from app.payment_readiness import EVM_ADDRESS


def receiver_status() -> dict:
    address = os.getenv("X402_RECEIVER_ADDRESS", "").strip()
    valid = bool(address and EVM_ADDRESS.fullmatch(address))
    return {
        "configured": bool(address),
        "valid": valid,
        "address": address if valid else None,
        "private_key_required": False,
        "private_key_present": False,
        "receive_only": True,
        "settlement_enabled": False,
        "blockers": ([] if valid else ["receiver_wallet_not_configured_or_invalid"])
        + ["settlement_disabled"],
    }
