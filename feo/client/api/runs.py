from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Run, RunQueryResult


class RunAPI(BaseAPI):
    def get(
        self,
        slug: str | None = None,
        model_slug: str | None = None,
        scenario_slug: str | None = None,
        owner_id: str | None = None,
        featured: bool | None = None,
        includes: str | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> List[Run]:
        params = {
            "slug": slug,
            "model_slug": model_slug,
            "scenario_slug": scenario_slug,
            "owner_id": owner_id,
            "featured": featured,
            "includes": includes,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/runs", params=params)
        resp.raise_for_status()

        return RunQueryResult(**resp.json()).runs
