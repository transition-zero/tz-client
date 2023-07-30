from typing import List, Optional, TypeVar

from pydantic import BaseModel

from feo.client import AssetCollection
from feo.client.base import Base

# use property decorator to facilitate getting and setting property

Cls = TypeVar("Cls", bound="Node")


class Alias(BaseModel):
    node_id: str
    alias: str
    node_level: str

    def node(self):
        return Node(id=self.node_id)


class Node(Base):
    def __init__(self, id, sectors, geometry, technologies):
        self.id = id
        self.sectors = sectors
        self.geometry
        self.technologies

        # Lazy populate assets
        self._assets: Optional[AssetCollection] = None

    @property
    def assets(self) -> AssetCollection:
        # assets getter to lazily retrieve assets
        if self._assets is None:
            # get asset collection
            self._assets = AssetCollection(node_id=self.node_id, sector=self.sector)
        else:
            return self._assets

    def json(self):
        return dict(
            node_id=self.node_id,
            sectors={k: s.json() for k, s in self.sectors.items()},
            # metadata
        )

    def children(self, node_level=None):
        # get heirarchical children for node
        pass

    def parents(self, node_level=None):
        # get heirarchical parents for node
        pass

    @classmethod
    def _get(cls, node_ids):
        # TODO
        pass

    @classmethod
    def search(cls, alias: str, threshold=0.95, node_level=None) -> List[Alias]:
        # call alias API
        pass

    @classmethod
    def from_alias(cls, alias) -> Cls:
        node_codes = cls.search(alias, threshold=1.0)
        if len(node_codes) == 0:
            node_codes = cls.search(cls, alias)
            raise ValueError(
                f"Node with alias '{alias}' not found! Did you mean any of {node_codes}?"
            )
        return node_codes[0].node()

    @classmethod
    def from_list(cls, list_of_ids):
        pass

    @classmethod
    def from_json(cls, obj):
        return [cls(**item) for item in obj["nodes"]]

    def __repr__(self):
        # information rich
        return f"Node(node_id={self.node_id},sector={self.sector})"

    def __str__(self):
        # human-readable
        return f"Node(node_id={self.node_id},sector={self.sector})"
