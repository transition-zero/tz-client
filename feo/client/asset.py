from typing import List, Optional

import pandas as pd
from pydantic import root_validator

from feo.client import api
from feo.client.api import schemas


class Asset(schemas.NodeBase):
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

    @root_validator(pre=True)
    def maybe_initialise_from_api(cls, values):
        id = values.get("id")
        node_type = values.get("node_type")
        type_alias = values.get("type_alias")

        if id is not None and any([(node_type is None), (type_alias is None)]):
            # call from API
            node = api.assets.get(ids=id)[0]

            for key, val in node.model_dump().items():
                values[key] = val

            return values

        return values


class AssetCollectionRow(pd.Series):
    @property
    def _constructor(self):
        return AssetCollectionRow

    @property
    def _constructor_expanddim(self):
        return AssetCollection

    def to_assets(self):
        return Asset(
            asset_properties=schemas.asset_sector_lookup[self.sector](**self.to_dict()),
            **self.to_dict(),
        )


class AssetCollection(pd.DataFrame):
    _scope: Optional[schemas.AssetCollectionScope] = None
    _page: Optional[int] = None

    @property
    def _constructor(self):
        return AssetCollection

    @property
    def _constructor_sliced(self):
        return AssetCollectionRow

    @classmethod
    def from_parent_node(cls, node_id: str, sector: str = "power"):
        obj = cls._from_assets(api.assets.get(parent_node_id=node_id, sector=sector))
        obj._scope = schemas.AssetCollectionScope(parent_node_id=node_id, sector=sector)
        obj._page = 0
        return obj

    @classmethod
    def _from_assets(cls, assets: List[Asset]):
        return cls.from_records([asset.unpack() for asset in assets])

    def next_page(self):
        if not self._scope:
            raise ValueError("Cant iterate an unscoped AssetCollection")
        if self._scope.parent_node_id is None:
            raise ValueError("Cant iterate an AssetCollection without a parent id")
        new_collection = self.__class__._from_assets(
            api.assets.get(parent_node_id=self._scope.parent_node_id, page=self._page + 1)
        )
        self._page += 1

        self.__dict__.update(pd.concat([self, new_collection], ignore_index=True).__dict__)
        return len(new_collection)

    def to_assets(self):
        return [
            Asset(
                asset_properties=schemas.asset_sector_lookup[row["sector"]](**row),
                **row,
            )
            for idx, row in self.iterrows()
        ]
