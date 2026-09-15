# Phase 0 Production Audit

Date: 2026-09-15
Branch: `phase-0/audit`
Baseline: `main` at `d3c5378e9f999bd332a95f71b7a98cb884632409`

## Scope and evidence

This is the Phase 0 audit for the testnet-to-production program. No production payment or mainnet behavior is enabled by this phase.

The requested `codebasememory` MCP is not available in the current execution environment. Repository navigation was therefore performed through GitHub's repository tree and targeted file/symbol reads rather than blind filesystem grep/find.

A full local gitleaks/trufflehog history scan could not be executed through the available GitHub connector. Targeted GitHub code searches found no matches for `private_key`, `seed phrase`, `mnemonic`, `API_KEY`, or `TOKEN=` on the default branch. **This is not equivalent to a full-history secret scan.** A real gitleaks/trufflehog history scan remains a blocking Phase 0 requirement before production.

## Architecture map

### Entrypoints

- `app/main.py`: FastAPI API and dashboard. Its lifespan calls `init_db()`.
- `app/scout_main.py`: initializes the DB and runs `ScoutRunner.run_forever()`.
- `app/market_main.py`: initializes the DB and runs `MarketRunner.run_forever()`.

### Database

- `app/db.py`: SQLAlchemy engine/session and `Base.metadata.create_all()` based `init_db()`.
- `app/models.py`: `OpportunityRecord`, `ActivityEvent`, `LedgerEntry`, and `MarketMetric`.

### Workers

- `app/services/scout_runner.py`: Circle discovery ingestion. Its forever loop catches all exceptions and silently continues.
- `app/services/market_runner.py`: Open402 and Coinbase Bazaar ingestion plus demand-metric refresh. The adapter loop is not isolated per adapter in the current main branch; one adapter exception aborts the rest of that cycle. Its forever loop also catches and silently continues.
- `app/workers/recovery.py` and `app/workers/scout.py` also exist and require lifecycle review during infrastructure hardening.

### External adapters / payment-related modules

- `app/adapters/circle.py`
- `app/adapters/coinbase.py`
- `app/adapters/open402.py`
- `app/adapters/x402.py`
- `app/x402_dry_run.py`
- `app/x402_accepts_preview.py`
- `app/x402_facilitator.py`
- `app/payment_offer_preview.py`
- `app/payment_readiness.py`
- `app/receiver_config.py`
- `app/test_buyer.py`
- `app/test_payer_config.py`

Current public/testnet payment endpoints advertise dry-run/testnet requirements and explicitly do not settle.

### API endpoints that write or can trigger work

Observed in `app/main.py`:

- `POST /api/market/metrics`: writes a `MarketMetric` and commits it.
- `POST /api/sandbox/{category}/run`: invokes sandbox service execution.
- `POST /api/evaluation/{category}`: invokes evaluation work and may perform service logic.

Several GET routes also trigger outbound/network work rather than being passive reads:

- `GET /api/research/liquidations/source-probe`
- `GET /api/prototype/liquidations/{asset}`
- `GET /api/validation/liquidations/{asset}`

The paid/testnet x402 routes currently return 402 offers but do not settle.

## Security-hardening patch status

**FAIL / NOT PRESENT on current main.**

The requested `fix/security-hardening` behavior is not present in the inspected baseline:

- `app/security.py` is absent from the repository tree.
- no `require_admin` symbol was found.
- no `PUBLIC_BASE_URL` symbol/configuration was found.
- `app/main.py` derives a public URL from `request.base_url` and rewrites HTTP to HTTPS.
- mutating and on-demand external-work endpoints have no admin dependency.

Per the production prompt, this hardening must be implemented before normal Phase 1 work. It should be delivered as its own security PR rather than mixed into this audit-only branch.

## Findings prioritized by risk

### CRITICAL

1. **Administrative authentication is absent.**
   Mutating POST routes and routes capable of initiating external work are reachable without `require_admin`. This is incompatible with production deployment.

2. **Public URL trust boundary is unsafe for payment requirements.**
   Payment resource URLs are derived from request metadata rather than a configured trusted `PUBLIC_BASE_URL`. Proxy/Host-header behavior must not control a payment destination/resource URL.

3. **Full-history secret scan is not yet proven.**
   Default-branch targeted searches found no obvious secret markers, but production cannot proceed until gitleaks or trufflehog scans the complete Git history.

### HIGH

4. **Schema creation is performed at application startup.**
   `Base.metadata.create_all()` is called by all three entrypoints. Production needs Alembic migrations and controlled schema rollout.

5. **Default database configuration is SQLite and Docker Compose contains static Postgres credentials.**
   Compose currently embeds `mitzu:mitzu`; production credentials must come from environment/secret management and Postgres must be production-only.

6. **Worker failure handling hides persistent outages.**
   `ScoutRunner.run_forever()` and `MarketRunner.run_forever()` swallow exceptions after `run_once()` fails. There is no bounded consecutive-failure policy, exponential backoff/jitter, or crash/alert threshold.

7. **Market adapter failures are not isolated.**
   The current `MarketRunner` wraps the complete adapter sequence in one try block. A failing adapter prevents later adapters and metric refresh from completing in that cycle.

8. **No production-grade rate limiting is visible.**
   Paid/pre-payment and external-call routes can be abused to amplify requests against upstream services/facilitators.

9. **No global exception-sanitization boundary is visible.**
   Production needs generic client errors and internal structured diagnostics without leaking httpx/SQLAlchemy details.

### MEDIUM

10. **Commercial readiness contains hardcoded positive evidence.**
    `/api/commercial-readiness/liquidations` passes `technical_validation="PASS"`, `observed_market_demand=True`, and `source_cost_verified=True` directly. These claims must derive from persisted evidence or be UNKNOWN.

11. **Dashboard/activity/error endpoints may disclose operational information.**
    `/api/activity`, `/api/errors`, and worker status expose internal messages. They need a data-exposure review before being public.

12. **Input validation is partly manual.**
    Asset allowlists and numeric clamps are implemented inside handlers. Production should use typed/Literal/range validation at the request boundary.

13. **N+1-style category processing exists.**
    Multiple endpoints enumerate categories and then call per-category service/scoring functions, creating avoidable query amplification.

14. **Dependencies use open lower bounds rather than a reproducible lock.**
    Production requires pinned/locked dependencies plus vulnerability auditing.

15. **Container/runtime hardening is incomplete.**
    Production requirements for non-root execution, healthcheck, proxy trust configuration, and restricted CORS/security headers are not evidenced in the inspected baseline.

## Positive controls already present

- Autonomous execution defaults to false.
- Wallet functionality defaults to false.
- Existing x402 endpoint behavior is explicitly dry-run/testnet and non-settling.
- The ledger distinguishes `verified` revenue.
- Test-payer and receiver configuration modules already separate payment experiments from the API.
- Git history shows prior safety-oriented x402 work and tests, including fail-closed facilitator/test-payer changes.

## Phase 0 gate status

**STOP — HUMAN REVIEW REQUIRED.**

Do not proceed to mainnet or production settlement.

Before Phase 1 can be treated as unblocked:

1. Review and approve this audit.
2. Implement the missing security-hardening patch (`app/security.py`, fail-closed `require_admin`, trusted `PUBLIC_BASE_URL`) in a dedicated branch/PR.
3. Run a genuine full-history `gitleaks` or `trufflehog` scan in an environment with repository checkout/history access. Any detected credential stops work until it is revoked/rotated and removed according to incident procedure.

No wallet secret, private key, blockchain signature, deposit, trade, or outgoing transaction is required by this audit.
