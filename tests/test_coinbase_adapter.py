from app.adapters.coinbase import _usd_price

def test_usdc_atomic_price_is_converted_to_dollars():
    assert _usd_price({
        "amount": "10000",
        "asset": "0x833589fCD6eDb6E08f4C7c32D4f71B54bDA02913",
    }) == 0.01

def test_unknown_asset_is_not_assumed_to_be_usd():
    assert _usd_price({"amount": "10000", "asset": "unknown"}) == 0
