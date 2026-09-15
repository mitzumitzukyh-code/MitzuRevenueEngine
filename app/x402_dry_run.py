"""x402 v2 dry-run signaling for the liquidation prototype.

This deliberately advertises a non-payable placeholder requirement. It tests
HTTP 402 and discovery-compatible metadata without a receiver wallet,
signature verification, facilitator calls, or settlement.
"""
import base64
import json


def dry_run_payment_required(base_url: str, asset: str) -> tuple[dict, str]:
    resource_url = f"{base_url.rstrip('/')}/api/paid/liquidations/{asset}"
    requirement = {
        "x402Version": 2,
        "error": "PAYMENT-SIGNATURE header is required; settlement is disabled in dry-run mode",
        "resource": {
            "url": resource_url,
            "description": "Heuristic liquidation leverage bands from public OKX market data",
            "mimeType": "application/json",
            "serviceName": "Mitzu Liquidation Signals",
            "tags": ["crypto", "liquidations", "market-data", "sandbox"],
        },
        "accepts": [],
        "extensions": {
            "mitzuDryRun": {
                "enabled": True,
                "priceHypothesisUsd": "0.005",
                "walletConfigured": False,
                "settlementEnabled": False,
            }
        },
    }
    encoded = base64.b64encode(
        json.dumps(requirement, separators=(",", ":")).encode()
    ).decode()
    return requirement, encoded
