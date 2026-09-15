import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.logging_config import JsonFormatter, RequestIdMiddleware
import logging


def test_json_formatter_contains_request_id():
    formatter = JsonFormatter()
    record = logging.LogRecord("test", logging.INFO, __file__, 1, "hello", (), None)
    payload = json.loads(formatter.format(record))
    assert payload["message"] == "hello"
    assert "request_id" in payload


def test_request_id_is_returned():
    app = FastAPI()
    app.add_middleware(RequestIdMiddleware)
    @app.get("/")
    def root():
        return {"ok": True}
    response = TestClient(app).get("/", headers={"X-Request-ID": "abc-123"})
    assert response.headers["X-Request-ID"] == "abc-123"
