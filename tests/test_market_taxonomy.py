from app.market_taxonomy import functional_category

def test_exa_search_is_classified_as_search():
    assert functional_category(
        tags=["search", "ai", "web", "research"],
        description="Exa /search endpoint",
        resource="https://api.exa.ai/search",
    ) == "search"

def test_brand_only_exa_tag_uses_endpoint_semantics():
    assert functional_category(
        tags=["Exa"],
        description="Exa Search - Neural search across the web",
        resource="https://stableenrich.dev/api/exa/search",
    ) == "search"

def test_contents_endpoint_is_content():
    assert functional_category(
        tags=["Exa"],
        description="Retrieve content from URLs",
        resource="https://stableenrich.dev/api/exa/contents",
    ) == "content"

def test_unknown_brand_does_not_become_category():
    assert functional_category(
        tags=["VendorBrand"],
        description="Special proprietary operation",
        resource="https://vendor.example/v1/run",
    ) == "uncategorized"
