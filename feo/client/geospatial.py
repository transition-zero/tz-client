from typing import List, Optional, Union

from feo.client import api
from feo.client.api import schemas
from feo.client.api.geospatial import FEATURES_TIMEOUT


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
        timeout: Optional[int] = FEATURES_TIMEOUT,
    ) -> "Features":
        """Search for vector features

        Args:
            collection_id (str): The collection to search.
            feature_ids (str | List[str] | None): Specific feature ID(s) to filter by.
            geometry (schemas.Geometry | None): Constrain the search to features
                intersecting `geometry`.
            simplify (float | str | None): A simplification method to apply to the features.
                Either a float `tolerance` value or one of `centroid`, `representative_point`.
            clip (bool | None): Clip fetures by `geometry`. Default is False
            properties (Dict | None): Apply filtering based on feature property values.
            limit (int | None): Maximum features to return
            page (int | None): Page number. Use with limit to paginate through results.
            timeout (int, optional): Maximum duration (seconds) to wait for data to be received.

        Returns:
            Features: A collection of Feature objects returned by the search.

        Raises:
            ReadTimout: When the response time exceeds the 'timeout' value.
        """
        search_results = api.vectors.get_features(
            collection_id,
            feature_ids,
            geometry,
            simplify,
            clip,
            properties,
            limit,
            page,
            timeout,
        )

        return cls(**search_results.model_dump())


class Geometry(schemas.Geometry):
    @classmethod
    def get(
        cls,
        feature_id: str,
        collection_id: str = "admin-gadm",
        timeout: Optional[int] = FEATURES_TIMEOUT,
    ) -> "Geometry":
        """Get a geometry for a specific feature

        Args:
            feature_id (str): ID of feature e.g. a Node ID.
            collection_id (str, optional): Data collection to search. Defaults to "admin-gadm".
            timeout (int, optional): Maximum duration (seconds) to wait for data to be received.

        Returns:
            Geometry: The feature's Geometry.

        Raises:
            NoFeaturesFound: If a geometry cannot be found for the specified feature_id.
            ReadTimout: When the response time exceeds the 'timeout' value.
        """
        geom = api.vectors.get_geometry(
            collection_id=collection_id, feature_id=feature_id, timeout=timeout
        )

        return cls(**geom.model_dump())
