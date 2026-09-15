import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware

request_id_var = ContextVar("request_id", default="-")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "level": record.levelname, "logger": record.name, "message": record.getMessage(), "request_id": request_id_var.get()}
        worker = getattr(record, "worker", None)
        event = getattr(record, "event", None)
        if worker: payload["worker"] = worker
        if event: payload["event"] = event
        return json.dumps(payload, separators=(",", ":"))

def configure_logging():
    handler = logging.StreamHandler(sys.stdout); handler.setFormatter(JsonFormatter())
    root = logging.getLogger(); root.handlers = [handler]; root.setLevel(logging.INFO)

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = request.headers.get("x-request-id", "").strip()[:128] or str(uuid4())
        token = request_id_var.set(rid)
        try:
            response = await call_next(request); response.headers["X-Request-ID"] = rid; return response
        finally:
            request_id_var.reset(token)
