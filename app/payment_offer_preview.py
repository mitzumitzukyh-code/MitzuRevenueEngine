"""Preview a future x402 payment offer without making it payable."""
from app.payment_readiness import EVM_ADDRESS


def preview_payment_offer(receiver: str | None, price_atomic: str = "5000") -> dict:
    valid = bool(receiver and EVM_ADDRESS.fullmatch(receiver))
    offer = {
        "scheme": "exact",
        "network": "eip155:84532",
        "amount": price_atomic,
        "asset": None,
        "payTo": receiver if valid else None,
        "maxTimeoutSeconds": 60,
        "extra": {
            "currency": "USDC_TESTNET",
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
            "testnet_asset_contract_not_verified",
            "settlement_disabled",
        ],
    }
