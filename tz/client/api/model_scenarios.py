from tz.client.api.base import BaseAPI
# fmt: off
from tz.client.api.generated_schema import (DeleteResponse, ModelScenario,
                                            ModelScenarioCreate,
                                            ModelScenarioPagination)
from tz.client.api.utils import non_empty


class ModelScenarioAPI(BaseAPI):
    def get(
        self,
        owner: str,
        model_slug: str,
        model_scenario_slug: str,
        includes: str | None = None,
    ) -> ModelScenario:
        params = {
            "includes": includes,
        }

        resp = self.client.get(
            f"/model-scenarios/{owner}:{model_slug}:{model_scenario_slug}", params=params
        )
        resp.raise_for_status()

        return ModelScenario(**resp.json())

    def create(self, model_scenario: ModelScenarioCreate) -> ModelScenario:
        resp = self.client.post("/model-scenarios", json=model_scenario.model_dump())
        resp.raise_for_status()
        return ModelScenario(**resp.json())

    def delete(self, owner: str, model_slug: str, slug: str) -> DeleteResponse:
        resp = self.client.delete(f"/model-scenarios/{owner}:{model_slug}:{slug}")
        resp.raise_for_status()
        return DeleteResponse(**resp.json())

    def search(
        self,
        model_scenario_slug: str | None = None,
        model_slug: str | None = None,
        includes: str | None = None,
        owner_id: str | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> list[ModelScenario]:
        params = {
            "model_scenario_slug": model_scenario_slug,
            "model_slug": model_slug,
            "includes": includes,
            "owner_id": owner_id,
            "featured": featured,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/model-scenarios", params=non_empty(params))
        resp.raise_for_status()

        r = ModelScenarioPagination(**resp.json())
        if r.model_scenarios:
            return r.model_scenarios
        else:
            return []
