from app.x402_accepts_preview import build_accepts_preview


def test_accepts_preview_is_complete_but_inert():
    result = build_accepts_preview()
    offer = result["accepts"][0]
    assert result["x402Version"] == 2
    assert offer["scheme"] == "exact"
    assert offer["network"] == "eip155:84532"
    assert offer["amount"] == "5000"
    assert offer["asset"] == "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    assert offer["payTo"] == "0xd108F49ca29eb1515aE28F345FCa29423F7Bb1d7"
    assert result["advertised_to_clients"] is False
    assert result["settlement_enabled"] is False
    assert result["real_funds"] is False
