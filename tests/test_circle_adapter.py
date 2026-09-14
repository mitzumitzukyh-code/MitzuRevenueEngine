import pytest
from app.adapters.circle import CircleDiscoveryAdapter

def test_adapter_name():
    assert CircleDiscoveryAdapter("https://example.invalid").name == "circle_x402"
