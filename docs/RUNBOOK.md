# Operations Runbook

## Security baseline

Production configuration is fail-closed. Set secrets through the deployment platform/environment only; never commit them.

Required security configuration includes ADMIN_KEY, PUBLIC_BASE_URL, DATABASE_URL and Postgres credentials. PUBLIC_BASE_URL must be HTTPS in production. CORS is disabled unless CORS_ORIGINS explicitly lists allowed origins.

The application has an in-process IP/route limiter. This is a defensive baseline for a single API process; a horizontally scaled deployment must replace it with a shared limiter at the reverse proxy or shared datastore.

Do not trust forwarded client-IP headers unless the deployment has a known reverse proxy and TRUST_PROXY_HEADERS is explicitly enabled. Uvicorn/reverse-proxy forwarded-allow configuration must be restricted to that proxy at deployment time.

## CI security gates

Every PR must pass ruff, pytest, pip-audit and gitleaks. Gitleaks checks full history because checkout uses fetch-depth 0.

## Production payment safety

This phase does not enable mainnet settlement. Keep autonomous spending, wallet signing and outgoing transactions disabled. Public receive-only addresses are not secrets; private keys, seeds and signer credentials must never be placed in this service.
