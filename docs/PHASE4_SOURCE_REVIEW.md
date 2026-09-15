# Phase 4 — Source and Redistribution Review

Date: 2026-09-15

## Decision gate

The collector MUST NOT ingest a venue into a paid x402 response merely because its API is public. Commercial redistribution/derived-work rights are a separate requirement. Sources remain disabled until their current terms grant the required rights or written permission is obtained.

## Reviewed sources

| Source | Public API technically available | Commercial redistribution into paid product | Decision |
|---|---|---|---|
| Coinbase Market Data | Yes | No without prior express written consent. Current Market Data Terms (updated 2026-08-07) restrict use to personal/research purposes and prohibit redistribution/display/dissemination of Market Data and Derived Works to third parties. | EXCLUDE |
| Deribit | Yes | No without prior written approval. Current membership terms state market and derived data are personal-use only and may not be aggregated, resold, published, forwarded, or otherwise processed beyond personal use without approval. | EXCLUDE |
| Kraken | Yes | Not established for the intended paid redistribution. A current Kraken MENA market rule surfaced an explicit written-authorization requirement for collecting/redistributing MTF market data; this is not sufficient permission for our use. | EXCLUDE pending written permission/clear license |
| Binance | Yes. Official 2026 developer docs expose public market-data endpoints. | NOT VERIFIED. Public API availability is not a redistribution license, and the official sources reviewed did not establish an affirmative right to resell/redistribute the required market/derived data. | EXCLUDE pending written permission/clear license |
| OKX | Yes | Previously reviewed terms prohibit redistribution/commercial data-product use without consent. | EXCLUDE |
| Bybit | Yes | Previously reviewed API terms prohibit repackaging/resale/commercial exploitation without permission. | EXCLUDE |

## Official sources used

- Coinbase Market Data Terms: https://www.coinbase.com/legal/market_data (updated 2026-08-07; sections 2–3).
- Deribit Exchange Membership Terms: https://support.deribit.com/hc/en-us/articles/25944532191645-Deribit-Exchange-Membership-Terms-Deribit-FZE (clause 2.10).
- Binance Developer REST API docs: https://developers.binance.com/en/docs/products/spot/rest-api (public market-data endpoint documented; no affirmative redistribution right established by this review).
- Kraken API overview: https://www.kraken.com/features/trading-api (technical availability only; not a redistribution grant).

## Consequence for product design

The proposed multi-exchange liquidation/funding/OI product cannot honestly be wired to payment yet. The blocker is licensing, not implementation capability. Building the collector against excluded sources now would create code whose intended paid use conflicts with, or is not affirmatively supported by, the reviewed terms.

A compliant next path is one of:

1. obtain explicit written redistribution/commercial-use permission from one or more venues; or
2. replace venue-owned feeds with a source whose license expressly permits commercial redistribution and derived analytics, then record that license/version here before implementation.

## Proposed response schema (NOT live; no fabricated observations)

The following is a schema example only. Numeric observations are intentionally null until a permitted collector has measured them.

```json
{
  "symbol": "BTC",
  "window": "1h",
  "observed": {
    "liquidation_notional_usd": null,
    "long_liquidation_notional_usd": null,
    "short_liquidation_notional_usd": null,
    "funding": null,
    "open_interest": null
  },
  "coverage": {
    "sources_expected": [],
    "sources_observed": [],
    "coverage_status": "BLOCKED_PENDING_LICENSE"
  },
  "methodology": "Aggregates only observations from sources licensed for commercial redistribution; no extrapolated exchange values.",
  "financial_advice": false
}
```

## STOP gate result

BLOCKED_PENDING_LICENSE. Do not implement or connect the paid collector until the source-rights blocker is resolved and explicitly approved at the Phase 4 human gate.
