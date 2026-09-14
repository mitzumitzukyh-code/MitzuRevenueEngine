"""Conservative taxonomy for public x402 marketplace listings.

The Bazaar tags field is free-form and frequently contains vendor/brand names.
This module prefers functional categories so demand is aggregated by what a
service does rather than who sells it.
"""
from urllib.parse import urlparse

_GENERIC_TAGS = {
    "search": "search",
    "web": "search",
    "research": "research",
    "crawler": "crawl",
    "crawling": "crawl",
    "scrape": "crawl",
    "scraping": "crawl",
    "contents": "content",
    "content": "content",
    "extraction": "content",
    "extract": "content",
    "enrichment": "enrichment",
    "people": "enrichment",
    "company": "enrichment",
    "finance": "finance",
    "financial": "finance",
    "crypto": "crypto",
    "blockchain": "crypto",
    "trading": "trading",
    "news": "news",
    "social": "social",
    "email": "email",
    "seo": "seo",
    "inference": "inference",
    "llm": "inference",
    "image": "media",
    "video": "media",
    "audio": "media",
    "payment": "payments",
    "payments": "payments",
    "checkout": "payments",
}

_KEYWORDS = (
    (("search", "query the web", "web search", "/search"), "search"),
    (("crawl", "scrape", "crawler"), "crawl"),
    (("contents", "content from urls", "extract full text", "/contents"), "content"),
    (("enrich", "lead discovery", "people search", "company search"), "enrichment"),
    (("liquidation",), "liquidations"),
    (("news",), "news"),
    (("token", "wallet", "blockchain", "ethereum", "solana"), "crypto"),
    (("payment", "checkout", "payee"), "payments"),
    (("seo", "robots.txt"), "seo"),
    (("inference", "llm", "model"), "inference"),
)

def functional_category(*, tags: list | None, description: str, resource: str) -> str:
    normalized_tags = [str(tag).strip().lower() for tag in (tags or []) if str(tag).strip()]
    for tag in normalized_tags:
        if tag in _GENERIC_TAGS:
            return _GENERIC_TAGS[tag]

    haystack = f"{description} {resource} {urlparse(resource).path}".lower()
    for needles, category in _KEYWORDS:
        if any(needle in haystack for needle in needles):
            return category

    return "uncategorized"
