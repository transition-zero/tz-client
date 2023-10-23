from typing import List, Optional, TypeVar

from pydantic import root_validator

# from feo.client.base import Base
from feo.client import api, schemas
from feo.client.asset import AssetCollection

# use property decorator to facilitate getting and setting property

Cls = TypeVar("Cls", bound="Node")


class Node(schemas.Node):
    geography: Optional[str] = None
    _assets: Optional[schemas.AssetCollection] = None

    @classmethod
    def search(
        cls, alias: str, threshold: int = 0.5, node_type: str = None
    ) -> List["Node"]:
        search_results = api.aliases.get(
            alias=alias, threshold=threshold, node_type=node_type, includes="node"
        )

        return [cls(alias["node"]) for alias in search_results["aliases"]]

    @root_validator(pre=True)
    def maybe_initialise_from_api(cls, values):
        id = values.get("id")
        node_type = values.get("node_type")
        type_alias = values.get("type_alias")
        geography = values.get("geography")

        if id is not None and any([(node_type is None), (type_alias is None)]):
            # call from API
            node = api.nodes.get(id=id)

            for key, val in node.items():
                values[key] = val

            return values

        elif id is None and geography is not None:
            node = api.aliases.get(alias=geography, includes="node")

            for key, val in node.items():
                values[key] = val

            return values

    @property
    def assets(self) -> AssetCollection:
        # lazily retrieve assets
        if self._assets is None:
            self._assets = AssetCollection.from_parent_node(node_id=self.id)
        else:
            return self.assets

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
    def from_list(cls, list_of_ids):
        pass
