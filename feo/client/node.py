from typing import Any, Dict, Optional, TypeVar

from pydantic import root_validator

# from feo.client.base import Base
from feo.client import api
from feo.client.api import schemas
from feo.client.asset import AssetCollection

# use property decorator to facilitate getting and setting property

Cls = TypeVar("Cls", bound="Node")


class Node(schemas.NodeBase):

    """
    The Node class enables access to geospatially-referenced data of a given node.
    Nodes are the fundamental building blocks of systems models, and can represent
    administrative areas like countries or continents, or physical assets like
    power stations or substations. TransitionZero indexes all data to nodes so
    it can easily be used to design and validate systems models.

    Nodes can be loaded directly with their id:

    ```python
    germany = Node("DEU")
    ```

    Nodes can also be retrieved by calling a well-known alias:

    ```python
    germany = Node("germany")
    ```
    """

    _geometry: Optional[str] = None
    _assets: Optional[AssetCollection] = None
    _children: Optional[list["Node"]] = None
    _parents: Optional[list["Node"]] = None
    _gross_capacity: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None

    def __init__(self, id: str, **kwargs) -> None:
        """Initialise Node from `id` as a positional argument"""
        super(self.__class__, self).__init__(id=id, **kwargs)

    @classmethod
    def search(
        cls, alias: str, threshold: float = 0.5, node_type: str | None = None
    ) -> list["Node"]:
        """
        Search for nodes using an alias.

        Args:
            alias (str): The target alias to search.
            threshold (float): The desired confidence in the search result.
            node_type (str): filter search to a specific node type.

        Returns:
            List[Node]: A list of Node objects.
        """

        search_results = api.aliases.get(
            alias=alias, threshold=threshold, node_type=node_type, includes="node"
        )

        return [
            cls(**alias.node.model_dump())  # type: ignore[union-attr]
            for alias in search_results.aliases
        ]

    @root_validator(pre=True)
    def maybe_initialise_from_api(cls, values):
        id = values.get("id")
        node_type = values.get("node_type")
        type_alias = values.get("type_alias")
        geography = values.get("geography")

        if id is not None and any([(node_type is None), (type_alias is None)]):
            # call from API

            node = api.nodes.get(ids=id)[0]

            for key, val in node.model_dump().items():
                values[key] = val

            return values

        elif id is None and geography is not None:
            node = api.aliases.get(alias=geography, includes="node")

            for key, val in node.items():
                values[key] = val

            return values

        return values

    @property
    def assets(self) -> AssetCollection:
        """An collection of assets located in (or connected to) this node."""
        if self._assets is None:
            self._assets = AssetCollection.from_parent_node(node_id=self.id)
            return self._assets
        else:
            return self.assets

    @classmethod
    def _get_children(cls, ids):
        node_data = api.nodes.get(ids=ids, includes="node.children")
        return node_data[0].children

    @classmethod
    def _get_parents(cls, ids):
        node_data = api.nodes.get(ids=ids, includes="node.parents")
        return node_data[0].parents

    @property
    def children(self) -> list["Node"]:
        """A set of nodes which are the heirarchical children of this node."""
        if self._children is None:
            self._children = self._get_children(self.id)
            return self._children
        else:
            return self._children

    @property
    def parents(self) -> list["Node"]:
        """A set of nodes which are the heirarchical ancestors of this node."""
        if self._parents is None:
            self._parents = self._get_parents(self.id)
            return self._parents
        else:
            return self._parents

    @classmethod
    def _get_geometry(cls, ids):
        raise NotImplementedError

    @property
    def geometry(self) -> str | Any:
        """The WGS84 GeoJSON for this node's geometry"""
        if self._geometry is None:
            self._geometry = self._get_geometry(self.id)
            return self._geometry
        else:
            return self._geometry
