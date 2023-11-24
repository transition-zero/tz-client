from datetime import datetime
from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Run, RunQueryResult


class RunAPI(BaseAPI):
    def get(
        self,
        fullslug: str,
        includes: str | None = None,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> Run:
        params = {
            "fullslug": fullslug,
            "includes": includes,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }

        resp = self.client.get(f"/runs/{fullslug}", params=params)
        resp.raise_for_status()

        return Run(**resp.json())

    def search(
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
