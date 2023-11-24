from copy import deepcopy

import pandas as pd

from feo.client import AssetCollection


def test_asset_collection():
    collection = AssetCollection.from_parent_node("IDN")

    # check datatype
    assert isinstance(collection, pd.DataFrame)

    collection_copy = deepcopy(collection)

    # roundtrip the asset conversion and back
    assert collection_copy.drop(columns=["children", "parents"]).equals(
        AssetCollection.from_assets(collection_copy.to_assets())
    )

    collection.next_page()

    # check our iteration
    assert len(collection) / len(collection_copy) == 2.0
