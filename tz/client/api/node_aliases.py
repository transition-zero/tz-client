from typing import Optional

from tz.client.api.base import BaseAPI
from tz.client.api.generated_schema import NodeAlias, NodeAliasPagination


class NodeAliasAPI(BaseAPI):
    def get_primary(self, node_slug: str) -> Optional[NodeAlias]:
        params = {"slug": node_slug, "primary": True, "limit": 1}

        resp = self.client.get("/node-aliases", params=params)
        resp.raise_for_status()

        paged = NodeAliasPagination(**resp.json())

        if paged.node_aliases and len(paged.node_aliases) == 1:
            return paged.node_aliases[0]
        else:
            raise ValueError(f"Couldn't locate primary node alias for node_slug={node_slug}")
