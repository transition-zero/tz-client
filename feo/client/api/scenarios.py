from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Scenario, ScenarioQueryResult


class ScenarioAPI(BaseAPI):
    def get(
        self,
        fullslug: str,
        includes: str | None = None,
    ) -> Scenario:
        params = {
            "includes": includes,
        }

        resp = self.client.get(f"/scenarios/{fullslug}", params=params)
        resp.raise_for_status()

        return Scenario(**resp.json())

    def search(
        self,
        scenario_slug: str | None = None,
        model_slug: str | None = None,
        includes: str | None = None,
        owner_id: str | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> List[Scenario]:
        params = {
            "scenario_slug": scenario_slug,
            "model_slug": model_slug,
            "includes": includes,
            "owner_id": owner_id,
            "featured": featured,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/scenarios", params=params)
        resp.raise_for_status()

        return ScenarioQueryResult(**resp.json()).scenarios
