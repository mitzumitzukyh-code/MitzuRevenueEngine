import pytest
from app.config import settings
from app.notify.telegram import send_alert

@pytest.mark.asyncio
async def test_telegram_disabled_is_noop(monkeypatch):
    monkeypatch.setattr(settings, "telegram_enabled", False)
    assert await send_alert("test") is False
