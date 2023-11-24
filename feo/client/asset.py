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


class AssetCollection(pd.DataFrame):
    """An AssetCollection is an extention of a Pandas DataFrame.

    It can be used in precisely the same way as a Pandas DataFrame
    but has a few extra useful constructors.

    Args:
        _scope (schemas.AssetcollectionScope | None): params for generating api query for pagination
        _page (int | None): if generated from an API query, the current page of the query.
    """

    _scope: Optional[schemas.CollectionScope] = None
    _page: Optional[int] = None

    @property
    def _constructor(self):
        return AssetCollection

    @property
    def _constructor_sliced(self):
        return AssetCollectionRow

    @classmethod
    def from_parent_node(cls, node_id: str, sector: str = "power"):
        """Instantiate an AssetCollection from a parent node.

        Args:
            node_id (str): the id of the parent node to retieve assets for.
            sector (str): the name of the sector to retireve assets for.

        Returns:
            AssetCollection: A pandas-dataframe extension for FEO assets.
        """

        obj = cls.from_assets(api.assets.get(parent_node_id=node_id, sector=sector))
        obj._scope = schemas.CollectionScope(parent_node_id=node_id, sector=sector)
        obj._page = 0
        return obj

    @classmethod
    def from_assets(cls, assets: List[Asset]):
        """Instiate an AssetCollection from a list of Assets.
        Unpacks `AssetProperties` to dataframe columns.
        """
        # pd.DataFrame.from_records
        return cls.from_records([asset.unpack() for asset in assets])

    def next_page(self):
        """Paginate through assets. The Asset collection must have a `_scope`.

        Returns the next page of assets and concatenates them in-place to the current collection.
        """
        if not self._scope:
            raise ValueError("Cant iterate an unscoped AssetCollection")
        if self._scope.parent_node_id is None:
            raise ValueError("Cant iterate an AssetCollection without a parent id")
        new_collection = self.__class__.from_assets(
            api.assets.get(parent_node_id=self._scope.parent_node_id, page=self._page + 1)
        )
        self._page += 1

        self.__dict__.update(pd.concat([self, new_collection], ignore_index=True).__dict__)
        return len(new_collection)

    def to_assets(self):
        """Instantiate a list of Assets from an AssetCollection.
        Re-packs `AssetProperties` on assets from dataframe columns.
        """
        return [
            Asset(
                asset_properties=schemas.asset_sector_lookup[row["sector"]](**row),
                **row,
            )
            for idx, row in self.iterrows()
        ]


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
