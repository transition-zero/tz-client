from typing import List

import pandas as pd

from feo.client import api
from feo.client.api import schemas


class Asset(schemas.NodeBase):
    @classmethod
    def from_id(cls, id: str):
        """Initialise Asset from `id` as a positional argument"""
        node = api.assets.get(ids=id)[0]
        return cls(**node.model_dump())

    def __init__(self, id: str, **kwargs):
        """Initialise Asset from `id` as a positional argument"""
        super(self.__class__, self).__init__(id=id, **kwargs)

    @classmethod
    def search(
        cls, alias: str, threshold: int = 0.5, node_type: str = None, sector: str = None
    ) -> List["schemas.Node"]:
        """
        Search for nodes using an alias.

        Args:
            alias (str): The target alias to search.
            threshold (float): The desired confidence in the search result.
            node_type (str): filter search to a specific node type.
            sector (str): the industrial sector to filter assets for

        Returns:
            List[Asset]: A list of Asset objects.
        """

        search_results = api.aliases.get(
            alias=alias, threshold=threshold, node_type=node_type, includes="power_unit"
        )

        return [cls(**alias.node.model_dump()) for alias in search_results.aliases]


class AssetCollection(pd.DataFrame):
    @classmethod
    def from_parent_node(cls, node_id: str):
        pass

    def next_page(self):
        pass
