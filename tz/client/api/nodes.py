from typing import Union

from tz.client.api.base import BaseAPI
from tz.client.api.generated_schema import Node


class NodeAPI(BaseAPI):
    def get(
        self,
        slug: str,
        includes: Union[str, None] = None,
    ) -> Node:
        params = dict(
            includes=includes,
        )

        resp = self.client.get(f"/nodes/{slug}", params=params)
        resp.raise_for_status()

        return Node(**resp.json())
