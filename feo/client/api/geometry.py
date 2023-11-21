from typing import List, Optional, Union

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Geometry, GeometryResponse


class GeometryAPI(BaseAPI):
    def get(
        self,
        collection_id: str,
        feature_ids: Optional[Union[str, List[str]]] = None,
        geometry: Optional[Geometry] = None,
        simplify: Optional[Union[float, str]] = None,
        clip: Optional[bool] = None,
        properties: Optional[dict] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GeometryResponse:
        if isinstance(feature_ids, list):
            feature_ids = ",".join(feature_ids)

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

        resp = self.client.get(f"/collections/{collection_id}/items", params=params)
        resp.raise_for_status()

        return GeometryResponse(**resp.json())
