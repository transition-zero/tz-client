from typing import Union

from tz.client.api.base import BaseAPI
from tz.client.api.generated_schema import NodeAliasPagination


class NodeAliasAPI(BaseAPI):
    def get(
        self,
        slug: str,
        threshold: Union[float, None] = None,
        node_type: Union[str, None] = None,
        sector: Union[str, None] = None,
        limit: Union[int, None] = None,
        page: Union[int, None] = None,
        includes: Union[str, None] = None,
    ) -> NodeAliasPagination:
        params = dict(
            slug=slug,
            threshold=threshold,
            node_type=node_type,
            sector=sector,
            page=page,
            limit=limit,
            includes=includes,
        )

        resp = self.client.get("node-aliases", params=params)
        resp.raise_for_status()

        return NodeAliasPagination(**resp.json())
