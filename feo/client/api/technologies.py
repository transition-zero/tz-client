from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Technology, TechnologyQueryResponse


class TechnologyAPI(BaseAPI):
    def get(self, slug: str) -> Technology:
        resp = self.client.get(f"/technologies/{slug}")
        resp.raise_for_status()

        return Technology(**resp.json())

    def search(
        self,
        uuid: str | None = None,
        slug: str | None = None,
        name: str | None = None,
        owner_id: str | None = None,
        public: bool | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> List[Technology]:
        params = {
            "uuid": uuid,
            "slug": slug,
            "name": name,
            "owner_id": owner_id,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/technologies", params=params)
        resp.raise_for_status()

        return TechnologyQueryResponse(**resp.json()).technologies
