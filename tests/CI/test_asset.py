import pytest

from feo.client import Asset, Node


@pytest.fixture
def asset():
    return Asset.from_id("PWRURNBGDA0U0")


class TestAsset:
    def test_search(self):
        items = Asset.search(alias="Rooppur nuclear power plant")
        assert isinstance(items, list)
        assert all(isinstance(asset, Asset) for asset in items)

    def test_search_with_sector(self):
        items = Asset.search(alias="Rooppur nuclear power plant", sector="power")
        assert isinstance(items, list)
        assert all(isinstance(asset, Asset) for asset in items)

    def test_properties(self, asset):
        assert asset.id == "PWRURNBGDA0U0"
        assert isinstance(asset.properties, dict | None)

    def test_asset_parents(node):
        parents = node.parents
        assert isinstance(parents, list)
        assert all(isinstance(parent, Node) for parent in parents)
