# from abc import classmethod

import pandas as pd

from feo.client import schemas


class Asset(schemas.Asset):
    def __init__(self, asset_id):
        pass

    @classmethod
    def search(cls, node_id, sector_id):
        pass


class AssetCollection(pd.DataFrame):
    @classmethod
    def from_parent_node(cls, node_id: str):
        pass

    def next_page(self):
        pass
