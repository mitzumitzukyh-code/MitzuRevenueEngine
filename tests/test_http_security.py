from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import settings
from app.middleware import RateLimitMiddleware, SecurityHeadersMiddleware


def test_security_headers_are_present(monkeypatch):
    monkeypatch.setattr(settings, "app_env", "production")
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware)

    @app.get("/")
    def root():
        return {"ok": True}

    response = TestClient(app).get("/")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "max-age=" in response.headers["strict-transport-security"]


def test_rate_limit_returns_429_and_retry_after(monkeypatch):
    monkeypatch.setattr(settings, "default_rate_limit_per_minute", 1)
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/limited")
    def limited():
        return {"ok": True}

    client = TestClient(app)
    assert client.get("/limited").status_code == 200
    response = client.get("/limited")
    assert response.status_code == 429
    assert int(response.headers["retry-after"]) >= 1
