from app.test_payer_config import test_payer_status as payer_status


def test_payer_secret_is_never_exposed(monkeypatch):
    monkeypatch.setenv("X402_TEST_PAYER_ADDRESS", "0x" + "2" * 40)
    monkeypatch.setenv("X402_TEST_PAYER_PRIVATE_KEY", "test-secret-never-return")
    result = payer_status()
    assert result["address_valid"] is True
    assert result["private_key_present"] is True
    assert result["private_key_exposed"] is False
    assert "test-secret-never-return" not in str(result)
    assert result["settlement_enabled"] is False
    assert result["real_funds"] is False


def test_missing_payer_cannot_sign(monkeypatch):
    monkeypatch.delenv("X402_TEST_PAYER_ADDRESS", raising=False)
    monkeypatch.delenv("X402_TEST_PAYER_PRIVATE_KEY", raising=False)
    result = payer_status()
    assert result["signing_enabled"] is False
    assert "test_payer_key_missing" in result["blockers"]
