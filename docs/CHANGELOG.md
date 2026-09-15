# Changelog

## Unreleased

### Phase 1 — security hardening
- Added fail-closed admin authentication with constant-time key comparison.
- Added trusted PUBLIC_BASE_URL for payment resource construction.
- Protected mutating and on-demand external-work endpoints.
- Added per-IP/per-route rate limiting with stricter pre-payment limits.
- Added closed-by-default CORS and security response headers.
- Removed static Postgres credentials from Compose.
- Hardened the API container to run non-root with a healthcheck.
- Added gitleaks and pip-audit CI gates.

No mainnet settlement, outgoing spending, or wallet signing was enabled.

### Phase 2 — reliable infrastructure
- Added Alembic and an initial schema migration.
- Production now rejects SQLite and no longer creates tables at API startup.
- Added configurable Postgres pooling/timeouts.
- Added bounded worker failure handling with exponential backoff.
- Added readiness checks for database connectivity and worker freshness.
- Documented daily backups and restoration drills.

### Phase 3 — data honesty
- Removed invented 20% unit-cost and 100-call demand assumptions from product planning.
- Commercial readiness now defaults unmeasured evidence to UNKNOWN and remains NOT_SELLABLE.
- Competition counts unique source/provider pairs instead of raw records.
- Renamed the bounty model to BountyOpportunity to distinguish it from the domain Opportunity model.

### Phase 4 — valuable product research
- Reviewed market-data redistribution constraints before collector implementation.
- Coinbase and Deribit are excluded from the paid product absent written permission; Binance and Kraken remain excluded until affirmative commercial redistribution rights are verified.
- Collector implementation is intentionally blocked at the Phase 4 human gate rather than building against legally unsuitable data sources.
