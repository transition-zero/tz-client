from typing import List, Union

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import AssetResponse, Node


class AssetAPI(BaseAPI):
    def get(
        self,
        ids: Union[str, List[str], None] = None,
        parent_node_id: Union[str, None] = None,
        sector: Union[str, None] = None,
        limit: Union[int, None] = None,
        page: Union[int, None] = None,
        includes: Union[str, None] = None,
    ) -> List[Node]:
        if isinstance(ids, list):
            ids = ",".join(ids)

        params = dict(
            id=ids,
            parent_node_id=parent_node_id,
            sector=sector,
            limit=limit,
            page=page,
            includes=includes,
        )

        resp = self.client.get("/assets", params=params)
        resp.raise_for_status()

        return AssetResponse(**resp.json()).assets
