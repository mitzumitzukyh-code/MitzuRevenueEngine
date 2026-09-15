import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        if settings.app_env.lower() == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Small in-process safety limiter; use a shared store when horizontally scaled."""

    def __init__(self, app):
        super().__init__(app)
        self._hits = defaultdict(deque)
        self._lock = Lock()

    async def dispatch(self, request: Request, call_next):
        limit = settings.prepayment_rate_limit_per_minute if request.url.path.startswith(("/api/paid/", "/api/testnet/paid/")) else settings.default_rate_limit_per_minute
        forwarded = request.headers.get("x-forwarded-for") if settings.trust_proxy_headers else None
        client_ip = (forwarded.split(",", 1)[0].strip() if forwarded else None) or (request.client.host if request.client else "unknown")
        key = (client_ip, request.url.path)
        now = time.monotonic()
        with self._lock:
            bucket = self._hits[key]
            while bucket and now - bucket[0] >= 60:
                bucket.popleft()
            if len(bucket) >= limit:
                retry_after = max(1, int(60 - (now - bucket[0])))
                return JSONResponse(status_code=429, content={"detail": "rate limit exceeded"}, headers={"Retry-After": str(retry_after)})
            bucket.append(now)
        return await call_next(request)
