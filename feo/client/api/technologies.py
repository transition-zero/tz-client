from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Technology, TechnologyQueryResponse


class TechnologyAPI(BaseAPI):
    def get(self, slug: str) -> Technology:
        resp = self.client.get(f"/technologies/{slug}")
        resp.raise_for_status()

        return TechnologyQueryResponse(**resp.json())

    def search(
        self,
        slug: str | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> List[Technology]:
        params = {
            "slug": slug,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/technologies", params=params)
        resp.raise_for_status()

        return TechnologyQueryResponse(**resp.json()).models
