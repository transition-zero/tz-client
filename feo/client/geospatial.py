from typing import List, Optional, Union

from feo.client import api
from feo.client.api import schemas


class Features(schemas.FeatureCollection):
    @classmethod
    def search(
        cls,
        collection_id: str,
        feature_ids: Optional[Union[str, List[str]]] = None,
        geometry: Optional[schemas.Geometry] = None,
        simplify: Optional[Union[float, str]] = None,
        clip: Optional[bool] = None,
        properties: Optional[dict] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ):
        search_results = api.vectors.get_features(
            collection_id,
            feature_ids,
            geometry,
            simplify,
            clip,
            properties,
            limit,
            page,
        )

        return cls(**search_results.model_dump())


class Geometry(schemas.Geometry):
    @classmethod
    def get(cls, feature_id: str, collection_id: str = "admin-gadm"):
        geom = api.vectors.get_geometry(collection_id=collection_id, feature_id=feature_id)

        return cls(**geom.model_dump())
