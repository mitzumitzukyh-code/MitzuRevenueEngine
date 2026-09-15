import httpx
from app.config import settings

async def send_alert(message: str) -> bool:
    if not settings.telegram_enabled:
        return False
    token = settings.telegram_bot_token.get_secret_value()
    chat_id = settings.telegram_chat_id.strip()
    if not token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json={"chat_id": chat_id, "text": message[:4000]})
        response.raise_for_status()
    return True
