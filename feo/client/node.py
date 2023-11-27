from typing import Dict, Optional

# from feo.client.base import Base
from feo.client import api
from feo.client.api import schemas
from feo.client.asset import AssetCollection
from feo.client.geospatial import Geometry

# use property decorator to facilitate getting and setting property


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

    _geometry: Optional[Geometry] = None
    _assets: Optional[AssetCollection] = None
    _children: Optional[list["Node"]] = None
    _parents: Optional[list["Node"]] = None
    _gross_capacity: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None

    @classmethod
    def from_id(cls, id: str) -> "Node":
        """Initialise Node from `id` as a positional argument"""
        node = api.nodes.get(ids=id)[0]
        return cls(**node.model_dump())

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

    @property
    def assets(self) -> AssetCollection:
        """An collection of assets located in (or connected to) this node."""
        if self._assets is None:
            self._assets = AssetCollection.from_parent_node(node_id=self.id)
        return self._assets

    @classmethod
    def _get_children(cls, ids):
        node_data = api.nodes.get(ids=ids, includes="node.children")
        return [cls(**child.model_dump()) for child in node_data[0].children]

    @classmethod
    def _get_parents(cls, ids):
        node_data = api.nodes.get(ids=ids, includes="node.parents")
        return [cls(**parent.model_dump()) for parent in node_data[0].parents]

    @property
    def children(self) -> list["Node"]:
        """A set of nodes which are the heirarchical children of this node."""
        if self._children is None:
            self._children = self._get_children(self.id)
            return self._children
        return self._children

    @property
    def parents(self) -> list["Node"]:
        """A set of nodes which are the heirarchical ancestors of this node."""
        if self._parents is None:
            self._parents = self._get_parents(self.id)
            return self._parents
        return self._parents

    @classmethod
    def _get_geometry(cls, ids) -> Geometry:
        return Geometry.get(ids)

    @property
    def geometry(self) -> Geometry:
        """The WGS84 GeoJSON for this node's geometry"""
        if self._geometry is None:
            self._geometry = self._get_geometry(self.id)
            return self._geometry
        else:
            return self._geometry
