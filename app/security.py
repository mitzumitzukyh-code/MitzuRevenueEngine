import secrets

from fastapi import Header, HTTPException, status

from app.config import settings


def require_admin(x_admin_key: str | None = Header(default=None, alias="X-Admin-Key")) -> None:
    """Fail closed unless the configured admin key matches in constant time."""
    expected = settings.admin_key.get_secret_value()
    if not expected or not x_admin_key or not secrets.compare_digest(x_admin_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unauthorized",
            headers={"WWW-Authenticate": "X-Admin-Key"},
        )


def public_base_url() -> str:
    """Return the trusted externally configured base URL; never derive it from Host headers."""
    value = settings.public_base_url.strip().rstrip("/")
    if not value:
        raise HTTPException(status_code=503, detail="public service URL is not configured")
    if settings.app_env.lower() == "production" and not value.startswith("https://"):
        raise HTTPException(status_code=503, detail="public service URL is not configured securely")
    return value
