from typing import Self

import pandas as pd
from pydantic import BaseModel


class Asset(Base):

    def __init__(self, asset_id):

    technology
    owner
    activity

    @classmethod
    def search(cls, node_id, sector_id) -> List[Self]






class AssetCollection(Base):

    def __init__(self, node_id:str, sector: str):
        self.node_id = node_id
        self.sector=sector
        self._assets = Asset.search(node_id=node_id, sector=sector)

    def __get_item__(self,i):

        return self._assets[i]

    def to_dataframe(self):
        return pd.DataFrame([a.json() for a in self._assets])


    def json(self):
        pass


    def __repr__(self):
        return f"AssetCollect(node_id={self.node_id},link_id={self.link_id},node_level={self.node_level},sector={self.sector})"

    def __str__(self):
        return f"AssetCollect(node_id={self.node_id},link_id={self.link_id},node_level={self.node_level},sector={self.sector}) with {len(self._assets)} assets"

    @classmethod
    def reduce_technologies(cls: str, node_id:str, sector:str) -> List[Technologies]:
        Base().client.get("")
