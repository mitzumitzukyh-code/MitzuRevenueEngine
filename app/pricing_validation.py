"""Evidence-based pricing validation for x402 data products."""
from dataclasses import asdict, dataclass
from statistics import median


@dataclass(frozen=True)
class ComparablePrice:
    provider: str
    product: str
    price_usd: float
    evidence_url: str
    evidence_kind: str


@dataclass(frozen=True)
class PricingValidation:
    product: str
    comparable_count: int
    min_price_usd: float
    median_price_usd: float
    max_price_usd: float
    recommended_entry_price_usd: float
    verdict: str
    rationale: str
    comparables: list[ComparablePrice]


def validate_liquidations_pricing() -> dict:
    # Publicly observable asking prices, not proof of buyer willingness to pay.
    comparables = [
        ComparablePrice(
            provider="Central Command",
            product="liquidation-heatmap",
            price_usd=0.005,
            evidence_url="https://www.x402-list.com/services/central-command",
            evidence_kind="PUBLIC_402_PRICE",
        ),
        ComparablePrice(
            provider="CryptoDataAPI",
            product="market-intelligence/liquidations",
            price_usd=0.01,
            evidence_url="https://cryptodataapi.com/blog/x402-pay-per-request-crypto-data-ai-agents",
            evidence_kind="PUBLIC_PROVIDER_PRICE",
        ),
        ComparablePrice(
            provider="LoneStarOracle",
            product="liquidations",
            price_usd=0.10,
            evidence_url="https://www.x402-list.com/services/lonestaroracle-liquidations",
            evidence_kind="PUBLIC_402_PRICE",
        ),
    ]
    prices = sorted(x.price_usd for x in comparables)
    market_median = median(prices)
    # Conservative launch hypothesis: match the cheapest close comparable.
    entry = prices[0]
    return asdict(PricingValidation(
        product="liquidations",
        comparable_count=len(comparables),
        min_price_usd=min(prices),
        median_price_usd=market_median,
        max_price_usd=max(prices),
        recommended_entry_price_usd=entry,
        verdict="PRICE_HYPOTHESIS",
        rationale=(
            "Public asking prices establish a defensible range but do not prove "
            "buyers will pay for this prototype. Keep pricing_validated=false "
            "until an actual paid request or equivalent buyer validation occurs."
        ),
        comparables=comparables,
    ))
