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
