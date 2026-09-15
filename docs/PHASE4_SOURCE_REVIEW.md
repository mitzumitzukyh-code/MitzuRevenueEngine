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

## Alternative-source review after human approval

### CoinGecko — potentially viable for a transformed analytics product, not raw resale

CoinGecko's current API materials distinguish commercial integration from redistribution. Its standard Commercial License says a product may charge users for its own services/products that incorporate or integrate CoinGecko API data, with prominent attribution, while raw API/data redistribution remains prohibited. CoinGecko's Data Redistribution / Data Reseller licenses are separate custom/Enterprise rights.

Official sources:
- https://www.coingecko.com/en/api
- https://www.coingecko.com/en/api/enterprise/data-license
- https://support.coingecko.com/hc/en-us/articles/16760512207257-What-Are-the-Differences-Between-Commercial-and-Custom-Licenses

Decision: BLOCKED_FOR_$0_PRODUCTION. Do not proxy, resell, sublicense or expose raw CoinGecko API access. CoinGecko's current pricing matrix explicitly assigns a Commercial license to paid plans, while the $0 Demo tier is described as testing/exploration and does not show a Commercial license. The keyless public API is explicitly described as optimized for low-volume testing and non-commercial educational use. Therefore neither zero-cost path is accepted for a paid Mitzu endpoint. A paid plan or separate written permission would violate the current no-spend constraint unless the human owner later authorizes it.

### DefiLlama — exclude

Current terms grant personal/non-commercial use and prohibit commercial exploitation, resale and republication without prior written consent. Decision: EXCLUDE absent written permission.

Official source: https://defillama.com/terms

### CoinCap — insufficient rights established

Current terms describe an API for use/display in external locations, but this review did not find an affirmative grant to resell or redistribute its data through a paid API. Decision: EXCLUDE_PENDING_CLEAR_LICENSE.

Official source: https://coincap.io/terms-of-service

## Product pivot candidate

Instead of selling raw exchange observations, Phase 4 should test a derived **market-risk snapshot** whose value is Mitzu's computation: normalized cross-asset volatility/regime metrics, market breadth, relative-volume/price dislocation and timestamped methodology. Source values are inputs; the response must not reproduce or proxy a source API. Every response must carry source attribution, observation window, freshness and `financial_advice: false`.

This pivot remains conceptually valid, but the reviewed CoinGecko zero-cost tiers do not satisfy the commercial-use gate. Current official pricing shows Demo at $0 with 10k calls/month and attribution, but Commercial licensing starts on paid plans; the keyless API is non-commercial. Therefore no CoinGecko collector will be implemented for the paid service under the current $0 constraint.

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

HUMAN_GATE_APPROVED_FOR_ALTERNATIVE_SOURCE_RESEARCH. Raw exchange redistribution remains blocked. CoinGecko is a constrained candidate for a transformed analytics product, but implementation is still gated on verifying that a zero-cost permitted tier covers the exact fields and commercial use. No subscription purchase is authorized.


## Zero-capital conclusion

As of this review, no reviewed market-data provider supplies both (a) the needed market inputs and (b) sufficiently explicit rights for a zero-cost paid API product. Phase 4 implementation is therefore intentionally blocked rather than silently converting a testing/free tier into commercial production use.

Next compliant revenue path: keep the market-data product blueprint dormant and redirect MITZU-001 toward externally funded software bounties/jobs that require no capital. Revenue from such work could later fund a properly licensed commercial data plan, subject to human approval before any spend.
