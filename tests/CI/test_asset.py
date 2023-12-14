import pytest
from httpx import HTTPStatusError

from feo.client import Asset


@pytest.fixture
def asset():
    return Asset.from_id("PWRURNBGDA0U0")


class TestAsset:
    def test_search(self):
        items = Asset.search(alias="Rooppur nuclear power plant")
        assert isinstance(items, list)
        assert all(isinstance(asset, Asset) for asset in items)

    def test_search_pagination(self):
        PAGE_LIMIT = 5
        items1 = Asset.search(alias="Rooppur nuclear power plant", limit=PAGE_LIMIT, page=0)
        assert len(items1) == PAGE_LIMIT
        items2 = Asset.search(alias="Rooppur nuclear power plant", limit=PAGE_LIMIT, page=1)
        assert len(items2) == PAGE_LIMIT
        items3 = Asset.search(alias="Rooppur nuclear power plant", limit=PAGE_LIMIT, page=2)
        assert len(items2) == PAGE_LIMIT

        # assert that no items are returned when page number is too high
        with pytest.raises(HTTPStatusError):
            Asset.search(alias="Rooppur", limit=PAGE_LIMIT, page=10000)

        ids1 = {item.id for item in items1}
        ids2 = {item.id for item in items2}
        ids3 = {item.id for item in items3}

        # check that there is no intersection between the sets by trying to find any matching ids
        assert ids1.intersection(ids2) == set()
        assert ids2.intersection(ids3) == set()
        assert ids1.intersection(ids3) == set()

    def test_search_with_sector(self):
        items = Asset.search(alias="Rooppur nuclear power plant", sector="power")
        assert isinstance(items, list)
        assert all(isinstance(asset, Asset) for asset in items)

    def test_properties(self, asset):
        assert asset.id == "PWRURNBGDA0U0"
        assert isinstance(asset.properties, dict | None)

    def test_str(self, asset):
        assert str(asset) == "Asset: Rooppur nuclear power plant - 2 (id=PWRURNBGDA0U0)"
