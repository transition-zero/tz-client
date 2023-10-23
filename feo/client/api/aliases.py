from typing import List, Union

from schemas import Alias

from feo.client.api.base import BaseAPI


class AliasAPI(BaseAPI):
    def get(
        self,
        alias: str,
        threshold: Union[float, None] = None,
        node_type: Union[str, None] = None,
        limit: Union[int, None] = None,
        page: Union[int, None] = None,
        includes: Union[str, None] = None,
    ) -> List[Alias]:
        params = dict(
            alias=alias,
            threshold=threshold,
            node_type=node_type,
            page=page,
            limit=limit,
        )

        resp = self.client.get("/aliases", params=params)
        resp.raise_for_status()

        return [Alias(**entry) for entry in resp.json()["aliases"]]
