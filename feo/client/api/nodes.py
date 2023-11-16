from typing import List, Union

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Node, NodeResponse


class NodeAPI(BaseAPI):
    def get(
        self,
        ids: Union[str, List[str]],
        includes: Union[str, None] = None,
    ) -> List[Node]:
        params = dict(
            includes=includes,
        )

        if isinstance(ids, list):
            ids = ",".join(ids)

        resp = self.client.get(f"/nodes/{ids}", params=params)
        resp.raise_for_status()

        return NodeResponse(**resp.json()).nodes
