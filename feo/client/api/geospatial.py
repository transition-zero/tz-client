from typing import List, Optional, Union

from httpx import ReadTimeout

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import FeatureCollection, Geometry

FEATURES_TIMEOUT = 30


class NoFeaturesFound(Exception):
    pass


class VectorAPI(BaseAPI):
    def get_features(
        self,
        collection_id: str,
        feature_ids: Optional[Union[str, List[str]]] = None,
        geometry: Optional[Geometry] = None,
        simplify: Optional[Union[float, str]] = 0.002,
        clip: Optional[bool] = None,
        properties: Optional[dict] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        timeout: Optional[int] = FEATURES_TIMEOUT,
    ) -> FeatureCollection:
        if isinstance(feature_ids, list):
            feature_ids = ",".join(feature_ids)

        if geometry is not None:
            geometry = geometry.to_geojson()

        params = dict(
            feature_ids=feature_ids,
            geometry=geometry,
            simplify=simplify,
            clip=clip,
            properties=properties,
            limit=limit,
            page=page,
        )

        params = {k: v for k, v in params.items() if v is not None}

        try:
            resp = self.client.get(
                f"/collections/{collection_id}/items", params=params, timeout=timeout
            )
            resp.raise_for_status()
        except ReadTimeout:
            raise ReadTimeout(
                f"Vector query timed out after {timeout}s. Try increasing the 'timeout' argument,"
                " particularly on slow connections"
            )

        return FeatureCollection(**resp.json())

    def get_geometry(
        self, feature_id: str, collection_id: str, timeout: Optional[int] = FEATURES_TIMEOUT
    ) -> Geometry:
        resp = self.get_features(
            collection_id=collection_id, feature_ids=[feature_id], timeout=timeout
        )

        try:
            ft = resp.features[0]
            return ft.geometry
        except IndexError:
            raise NoFeaturesFound(
                f"No features found for node '{feature_id}' in collection '{collection_id}'"
            )


class RasterAPI(BaseAPI):
    def get(self):
        raise NotImplementedError
