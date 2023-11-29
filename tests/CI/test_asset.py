import pytest

from feo.client import Asset


@pytest.fixture
def asset():
    return Asset.from_id("PWRURNBGDA0U0")


class TestAsset:
    def test_search(self):
        items = Asset.search(alias="Rooppur nuclear power plant")
        assert isinstance(items, list)
        assert all(isinstance(asset, Asset) for asset in items)

    @pytest.mark.skip(reason="edge case bug not resolved yet")  # FIXME
    def test_search_pagination(self):
        PAGE_LIMIT = 5
        items1 = Asset.search(alias="Rooppur nuclear power plant", limit=PAGE_LIMIT, page=0)
        assert len(items1) == PAGE_LIMIT
        items2 = Asset.search(alias="Rooppur nuclear power plant", limit=PAGE_LIMIT, page=1)
        assert len(items2) == PAGE_LIMIT

        # assert that no items are returned when page number is too high
        items_bad = Asset.search(alias="Rooppur", limit=PAGE_LIMIT, page=10000)
        assert len(items_bad) == 0

        ids1 = {item.id for item in items1}
        ids2 = {item.id for item in items2}
        # assert that items on different pages are all different
        assert ids1.intersection(ids2) == set()

    def test_search_with_sector(self):
        items = Asset.search(alias="Rooppur nuclear power plant", sector="power")
        assert isinstance(items, list)
        assert all(isinstance(asset, Asset) for asset in items)

    def test_properties(self, asset):
        assert asset.id == "PWRURNBGDA0U0"
        assert isinstance(asset.properties, dict | None)

    def test_str(self, asset):
        assert str(asset) == "Asset: Rooppur nuclear power plant - 2 (id=PWRURNBGDA0U0)"
