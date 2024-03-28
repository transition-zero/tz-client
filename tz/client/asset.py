from typing import ForwardRef, List

import pandas as pd

from tz.client import api
from tz.client.api import schemas
from tz.client.source import Source


class Asset(schemas.NodeBase):
    _source_objects: List[ForwardRef("Source")] | None = None  # type: ignore[valid-type] # noqa

    @classmethod
    def from_id(cls, id: str):
        """Initialise Asset from `id` as a positional argument"""
        node = api.assets.get(ids=id)[0]
        return cls(**node.model_dump())

    # Note: v2-migration - This needs to be revised; but I don't want to try
    # and get the types right just now, so commenting it out.
    # @classmethod
    # def search(
    #     cls,
    #     slug: str,
    #     threshold: float = 0.5,
    #     node_type: str | None = None,
    #     sector: str | None = None,
    #     limit: int = 10,
    #     page: int = 0,
    # ) -> list[generated_schema.Node]:
    #     """
    #     Search for nodes using an alias.

    #     Args:
    #         alias (str): The target alias to search.
    #         threshold (float): The desired confidence in the search result.
    #         node_type (str): filter search to a specific node type.
    #         sector (str): the industrial sector to filter assets for
    #         limit (int): The maximum number of search results to return per page.
    #         page (int): The page number of search results to return.

    #     Returns:
    #         list[schemas.Node]: A list of Node objects.
    #     """

    #     search_results = api.node_aliases.get(
    #         slug=slug,
    #         threshold=threshold,
    #         node_type=node_type,
    #         sector=sector,
    #         includes="power_unit",
    #         limit=limit,
    #         page=page,
    #     )

    #     return [
    #         cls(**alias.node.model_dump())  # type: ignore[union-attr, misc]
    #         for alias in search_results.node_aliases
    #     ]

    @property
    def sources(self):
        if self._source_objects is None:
            asset = api.assets.get(ids=self.id, includes="sources")[0]
            self._source_objects = [Source(**source.model_dump()) for source in asset.base_sources]
        return self._source_objects

    def __str__(self) -> str:
        return f"Asset: {self.name_primary_en} (id={self.id})"


class AssetCollection(pd.DataFrame):
    """An AssetCollection is an extension of a Pandas DataFrame.

    It can be used in precisely the same way as a Pandas DataFrame
    but has a few extra useful constructors.

    Args:
        _scope (schemas.AssetcollectionScope | None): params for generating api query for pagination
        _page (int | None): if generated from an API query, the current page of the query.
    """

    _scope: schemas.CollectionScope | None = None
    _page: int | None = None

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
            AssetCollection: A pandas-dataframe extension for TransitionZero assets.
        """

        obj = cls.from_assets(
            api.assets.get(parent_node_id=node_id, sector=sector)  # type: ignore[arg-type]
        )
        obj._scope = schemas.CollectionScope(parent_node_id=node_id, sector=sector)
        obj._page = 0
        return obj

    @classmethod
    def from_assets(cls, assets: List[Asset]):  # type: ignore[arg-type]
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
