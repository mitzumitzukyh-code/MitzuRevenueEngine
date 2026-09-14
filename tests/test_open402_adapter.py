from app.adapters.open402 import Open402DirectoryAdapter, _directory_items

def test_adapter_is_read_only_discovery():
    adapter = Open402DirectoryAdapter("https://example.invalid")
    assert adapter.name == "open402"
    assert not hasattr(adapter, "pay")
    assert not hasattr(adapter, "sign")

def test_directory_items_accepts_nested_data_envelope():
    payload = {"data": {"domains": [{"domain": "example.com"}]}, "pagination": {"total": 1}}
    assert _directory_items(payload) == [{"domain": "example.com"}]

def test_directory_items_accepts_services_and_filters_non_objects():
    payload = {"services": [{"origin": "api.example.com"}, "bad", None]}
    assert _directory_items(payload) == [{"origin": "api.example.com"}]
