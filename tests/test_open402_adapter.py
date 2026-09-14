from app.adapters.open402 import Open402DirectoryAdapter

def test_adapter_is_read_only_discovery():
    adapter = Open402DirectoryAdapter("https://example.invalid")
    assert adapter.name == "open402"
    assert not hasattr(adapter, "pay")
    assert not hasattr(adapter, "sign")
