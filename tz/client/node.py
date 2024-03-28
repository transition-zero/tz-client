from typing import Optional

from tz.client import api
from tz.client.api import generated_schema
from tz.client.utils import lazy_load_relationship


class Node(generated_schema.Node):

    """
    <!--
    The Node class enables access to geospatially-referenced data of a given node.
    Nodes are the fundamental building blocks of systems models, and can represent
    administrative areas like countries or continents, or physical assets like
    power stations or substations. TransitionZero indexes all data to nodes so
    it can easily be used to design and validate systems models.
    -->

    Nodes can be loaded directly with their slug:

    ```python
    germany = Node.from_slug("DEU")
    ```

    """

    _primary_node_alias: Optional[generated_schema.NodeAlias] = None
    _children: Optional[list["Node"]] = None
    _parents: Optional[list["Node"]] = None
    # _assets: Optional[AssetCollection] = None
    # _gross_capacity: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None

    @classmethod
    def from_slug(cls, slug: str) -> "Node":
        """Initialise Node from `slug` as a positional argument"""
        api_node = api.nodes.get(slug=slug, includes="aliases")
        node = cls(**api_node.model_dump())
        if node.aliases:
            maybe_primary = [
                alias
                for alias in node.aliases
                if isinstance(alias, generated_schema.NodeAlias) and alias.primary
            ]
            if len(maybe_primary) == 1:
                cls._primary_node_alias = maybe_primary[0]
        return node

    @classmethod
    def search(
        cls,
        slug: str,
        threshold: float = 0.5,
        node_type: str | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> list["Node"]:
        """
        Search for nodes using an alias.

        ```python
        germany_nodes = Node.search("Germany")
        ```

        Args:
            slug (str): The target slug to search.
            threshold (float): The desired confidence in the search result.
            node_type (str): filter search to a specific node type.
            limit (int): The maximum number of search results to return per page.
            page (int): The page number of search results to return.

        Returns:
            List[Node]: A list of Node objects.
        """

        search_results = api.node_aliases.get(
            slug=slug,
            threshold=threshold,
            node_type=node_type,
            includes="node",
            limit=limit,
            page=page,
        )

        return [
            cls(**alias.node.model_dump())  # type: ignore[union-attr]
            for alias in search_results.node_aliases  # type: ignore[union-attr]
        ]

    # @property
    # def assets(self) -> AssetCollection:
    #     """An collection of assets located in (or connected to) this node."""
    #     if self._assets is None:
    #         self._assets = AssetCollection.from_parent_node(node_id=self.id)
    #     return self._assets

    # @classmethod
    # def _get_children(cls, ids):
    #     node_data = api.nodes.get(ids=ids, includes="children")
    #     return [cls(**child.model_dump()) for child in node_data[0].children]

    # @classmethod
    # def _get_parents(cls, ids):
    #     node_data = api.nodes.get(ids=ids, includes="parents")
    #     return [cls(**parent.model_dump()) for parent in node_data[0].parents]

    # @property
    # def children(self) -> list["Node"]:
    #     """A set of nodes which are the heirarchical children of this node."""
    #     if self._children is None:
    #         self._children = self._get_children(self.id)
    #         return self._children
    #     return self._children

    # @property
    # def parents(self) -> list["Node"]:
    #     """A set of nodes which are the heirarchical ancestors of this node."""
    #     if self._parents is None:
    #         self._parents = self._get_parents(self.id)
    #         return self._parents
    #     return self._parents

    def __str__(self) -> str:
        alias_str = self._primary_node_alias.slug if self._primary_node_alias else ""
        return f"Node: {alias_str} (id={self.slug})"


lazy_load_relationship(
    Node,
    "children",
    lambda self: api.nodes.get(slug=self.slug, includes="children"),
)

lazy_load_relationship(
    Node,
    "parents",
    lambda self: api.nodes.get(slug=self.slug, includes="parents"),
)
