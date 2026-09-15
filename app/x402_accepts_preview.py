"""Build an x402 v2 accepts entry for testnet preview only."""
from app.payment_offer_preview import DEFAULT_TESTNET_RECEIVER

BASE_SEPOLIA = "eip155:84532"
USDC_BASE_SEPOLIA = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"


def build_accepts_preview() -> dict:
    return {
        "x402Version": 2,
        "accepts": [{
            "scheme": "exact",
            "network": BASE_SEPOLIA,
            "amount": "5000",
            "asset": USDC_BASE_SEPOLIA,
            "payTo": DEFAULT_TESTNET_RECEIVER,
            "maxTimeoutSeconds": 60,
            "extra": {"name": "USDC", "version": "2"},
        }],
        "advertised_to_clients": False,
        "settlement_enabled": False,
        "real_funds": False,
        "mode": "TESTNET_ACCEPTS_PREVIEW",
    }
