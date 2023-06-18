from datetime import date
from typing import List, Optional, Union

import httpx

from transitionzero.client import utils
from transitionzero.client.base import Base


class System(Base):
    def __init__(
        self,
        sectors: Union[List, str],
        geography: Optional[Union[List,str]],
        node_level: Optional[str],
        node_ids: Optional[Union[List,str]],
        links: Optional[str],
        link_ids: Optional[Union[List,str]]
    ):
        super().__init__()

        # some error checking
        if geography is not None and node_ids is not None:
            # NOT AND (geography, node_ids)
            raise ValueError("Only one of 'geography' and 'node_ids' can be specified. Refer to help(System) for more details.")
        if geography is not None and node_level is None:
            # AND (geography, node_level)
            raise ValueError("If specifying 'geography', 'node_level' must also be specified. Refer to help(System) for more details.")
        if geography is None and node_ids is None:
            # OR (geography, node_ids)
            raise ValueError("One of 'geography' or 'node_ids' must be specified. Refer to help(System) for more details.")

        if links is not None and link_ids is not None:
            raise ValueError("One of either 'links' or 'link_ids' must be provided")

        if links is not None:
            assert links in ["all", "neighbours"], "'links' must be one of ['all','neighbours']"

        # enforce lists
        sectors = utils.enforce_list(sectors) if sectors is not None else None
        geography = utils.enforce_list(geography) if geography is not None else None
        node_ids = utils.enforce_list(node_ids) if node_ids is not None else None
        link_ids = utils.enforce_list(link_ids) if link_ids is not None else None

        # populate node_ids if 'geography' is given:
        node_ids = self._get_node_ids(geography, node_level) if geography is not None else node_ids
        # populate link_ids if 'links' is given:
        link_ids = self._get_link_ids(links, node_ids) if links is not None else link_ids

    def _get_node_ids(self, geography, node_level):
        try:
            node_geo = Node(geography)
        except 404:
            node_alias = Node.search(geography)
            raise ValueError(f"Node alias '{geography}' not found. Did you mean one of {[a.name for a in node_alias]}? Try Node.search(...) for more help.")

        return node_geo.children(node_level=node_level)

    def _get_link_ids(self, links, node_ids):
        pass


    # self.nodes.sectors['power'].assets
    @property
    def sectors
