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


## Database migrations and backup

Production schema changes are applied with `alembic upgrade head` before application rollout. The API does not call `create_all` in production.

PostgreSQL backups must run daily using `pg_dump --format=custom` to encrypted deployment storage with retention appropriate to the hosting environment. Do not commit dumps or credentials. At least monthly, restore the newest backup into an isolated non-production Postgres instance using `pg_restore --clean --if-exists`, run `alembic upgrade head`, and verify row counts plus `/ready` before recording the restore drill as successful.

`/health` is process liveness. `/ready` checks database connectivity and worker freshness; a stale required worker returns 503.


## Telegram alerts

Telegram is opt-in. Set TELEGRAM_ENABLED=true plus TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID only in the deployment secret store. Test delivery after deployment without printing the token. Alert delivery failure must never enable spending or alter ledger state.

Operational alert conditions for the production deployment are: required worker stale beyond WORKER_STALE_AFTER_SECONDS; repeated worker failures reaching the configured limit; elevated API/adapter error rate; verified payment whose settlement later fails; kill switch activation; and the daily revenue/cost summary. Payment-specific alerts are wired when settlement exists in Phase 5; this phase only provides the notification transport.


## Data honesty gate

Commercial-readiness fields must be derived from persisted measurements or remain UNKNOWN. UNKNOWN is fail-closed and blocks SELLABLE status. Product costs, margins, call targets and profit projections must not be inferred from arbitrary ratios. Cost-based decisions remain disabled until measured infrastructure, facilitator, gas-if-applicable and paid-source costs are recorded.
