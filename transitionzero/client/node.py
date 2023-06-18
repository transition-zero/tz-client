from abc import classmethod

from feo.client.base import Base
from pydantic import BaseModel

# use property decorator to facilitate getting and setting property


class Alias(BaseModel):
    node_id: str
    alias: str
    node_level: str

class Node(Base):

    def __init__(self, node_id):
        self.node_id = node_id
        self.sectors = {
            key: NodeSector(sector=key)
        }
        self._fill_metadata()

    def _fill_metadata(self):
        # call API and fill metadata from response. e.g. node_level
        pass

    def json(self):
        return dict(
            node_id=self.node_id,
            sectors={k:s.json() for k,s in self.sectors.items()},
            # metadata
        )

    def children(self, node_level=None):
        # get heirarchical children for node

    def parents(self, node_level=None):
        # get heirarchical parents for node


    @classmethod
    def search(cls, alias:str, threshold=0.95, node_level=None) -> List[Alias]:
        # call alias API






class NodeSector(Base):
    def __init__(self,node_id, sector):
        self.node_id=node_id
        self.sector=sector

        # eagerly populate technologies
        self._technologies: List[Technology] = AssetCollection.reduce_technologies(node_id=self.node_id, sector=self.sector)

        # Lazy populate assets
        self._assets: Optional[AssetCollection] = None

    @property
    def assets(self) -> AssetCollection:
        # assets getter to lazily retrieve assets
        if self._assets=None:
            # get asset collection
            self._assets = AssetCollection(node_id=self.node_id, sector=self.sector)
        else:
            return self._assets


    def json(self):
        # make a json obj
        return dict(
            technologies={t.code:t.json() for t in self._technologies},
            assets = {a.id:a.json() for a in self.assets} if self._assets else None,
        )

    def __repr__(self):
        # information rich
        return f"NodeSector(node_id={self.node_id},sector={self.sector})"

    def __str__(self):
        # human-readable
        f"NodeSector(node_id={self.node_id},sector={self.sector})"
