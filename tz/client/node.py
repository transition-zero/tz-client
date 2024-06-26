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

    # _primary_node_alias: Optional[generated_schema.NodeAlias] = None
    _children: Optional[list["Node"]] = None
    _parents: Optional[list["Node"]] = None
    # _assets: Optional[AssetCollection] = None
    # _gross_capacity: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None

    @classmethod
    def from_slug(cls, slug: str) -> "Node":
        """Initialise Node from `slug` as a positional argument"""
        api_node = api.nodes.get(slug=slug, includes="primary_alias")
        node = cls(**api_node.model_dump())
        return node

    @classmethod
    def search(
        cls,
        name: str,
        threshold: float = 0.5,
        node_type: str | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> list["Node"]:
        """
        Search for nodes using an alias name.

        ```python
        germany_nodes = Node.search("Germany")
        ```

        Args:
            name (str): The target name to search.
            threshold (float): The desired confidence in the search result.
            node_type (str): filter search to a specific node type.
            limit (int): The maximum number of search results to return per page.
            page (int): The page number of search results to return.

        Returns:
            List[Node]: A list of Node objects.
        """

        search_results = api.node_aliases.get(
            name=name,
            threshold=threshold,
            node_type=node_type,
            includes="node,node.primary_alias",
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

    def __str__(self) -> str:
        alias_str = (
            f"primary-alias={self.primary_alias}"
            if self.primary_alias
            else "no primary alias found"
        )
        return f"Node: {alias_str} (fullslug={self.fullslug})"


lazy_load_relationship(
    Node,
    Node,
    "children",
    lambda self, _: api.nodes.get(slug=self.slug, includes="children"),
)

lazy_load_relationship(
    Node,
    Node,
    "parents",
    lambda self, _: api.nodes.get(slug=self.slug, includes="parents"),
)
