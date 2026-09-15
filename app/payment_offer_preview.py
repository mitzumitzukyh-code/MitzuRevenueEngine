"""Preview a future x402 payment offer without making it payable."""\n\nDEFAULT_TESTNET_RECEIVER = "0xd108F49ca29eb1515aE28F345FCa29423F7Bb1d7"
from app.payment_readiness import EVM_ADDRESS


def preview_payment_offer(receiver: str | None = DEFAULT_TESTNET_RECEIVER, price_atomic: str = "5000") -> dict:
    valid = bool(receiver and EVM_ADDRESS.fullmatch(receiver))
    offer = {
        "scheme": "exact",
        "network": "eip155:84532",
        "amount": price_atomic,
        "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
        "payTo": receiver if valid else None,
        "maxTimeoutSeconds": 60,
        "extra": {
            "currency": "USDC_TESTNET",
            "assetEvidence": "Circle official Base Sepolia USDC contract",
            "priceUsdHypothesis": "0.005",
        },
    }
    return {
        "mode": "PREVIEW_ONLY",
        "advertised_to_clients": False,
        "settlement_enabled": False,
        "offer": offer,
        "blockers": [
            *([] if valid else ["receiver_wallet_not_configured_or_invalid"]),
            "settlement_disabled",
        ],
    }
