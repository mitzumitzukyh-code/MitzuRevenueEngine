from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import settings
from app.security import public_base_url, require_admin


def _client() -> TestClient:
    app = FastAPI()

    @app.get("/admin", dependencies=[])
    def admin(_: None = __import__("fastapi").Depends(require_admin)):
        return {"ok": True}

    return TestClient(app)


def test_admin_auth_fails_closed_when_key_missing(monkeypatch):
    monkeypatch.setattr(settings, "admin_key", __import__("pydantic").SecretStr(""))
    assert _client().get("/admin").status_code == 401


def test_admin_auth_rejects_wrong_key(monkeypatch):
    monkeypatch.setattr(settings, "admin_key", __import__("pydantic").SecretStr("expected"))
    assert _client().get("/admin", headers={"X-Admin-Key": "wrong"}).status_code == 401


def test_admin_auth_accepts_matching_key(monkeypatch):
    monkeypatch.setattr(settings, "admin_key", __import__("pydantic").SecretStr("expected"))
    response = _client().get("/admin", headers={"X-Admin-Key": "expected"})
    assert response.status_code == 200


def test_public_base_url_is_explicit_not_request_derived(monkeypatch):
    monkeypatch.setattr(settings, "app_env", "production")
    monkeypatch.setattr(settings, "public_base_url", "https://api.example.test/")
    assert public_base_url() == "https://api.example.test"
