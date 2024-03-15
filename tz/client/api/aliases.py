from typing import Union

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import AliasResponse


class AliasAPI(BaseAPI):
    def get(
        self,
        alias: str,
        threshold: Union[float, None] = None,
        node_type: Union[str, None] = None,
        sector: Union[str, None] = None,
        limit: Union[int, None] = None,
        page: Union[int, None] = None,
        includes: Union[str, None] = None,
    ) -> AliasResponse:
        params = dict(
            alias=alias,
            threshold=threshold,
            node_type=node_type,
            sector=sector,
            page=page,
            limit=limit,
            includes=includes,
        )

        resp = self.client.get("/aliases", params=params)
        resp.raise_for_status()

        return AliasResponse(**resp.json())
