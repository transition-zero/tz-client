from copy import deepcopy

from feo.client import AssetCollection


def test_asset_collection():
    collection = AssetCollection.from_parent_node("IDN")

    # check datatype
    assert isinstance(collection)

    collection_copy = deepcopy(collection)

    # roundtrip the asset conversion and back
    assert collection_copy.drop(columns=["children", "parents"]).equals(
        AssetCollection.from_assets(collection_copy.to_assets())
    )

    collection.next()

    # check our iteration
    assert len(collection) / collection_copy == 2.0
