import base64
import json

from app.x402_dry_run import dry_run_payment_required


def test_dry_run_is_v2_and_cannot_settle():
    body, header = dry_run_payment_required("https://example.com", "BTC")
    decoded = json.loads(base64.b64decode(header).decode())
    assert body["x402Version"] == 2
    assert decoded == body
    assert body["accepts"] == []
    assert body["extensions"]["mitzuDryRun"]["walletConfigured"] is False
    assert body["extensions"]["mitzuDryRun"]["settlementEnabled"] is False
    assert body["extensions"]["mitzuDryRun"]["priceHypothesisUsd"] == "0.005"
