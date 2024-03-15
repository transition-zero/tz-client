from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Model, ModelQueryResult


class ModelAPI(BaseAPI):
    def get(self, slug: str, includes: str | None = None) -> Model:
        resp = self.client.get(f"/models/{slug}", params={"includes": includes})
        resp.raise_for_status()

        return Model(**resp.json())

    def search(
        self,
        model_slug: str | None = None,
        includes: str | None = None,
        owner: str | None = None,
        sort: str | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> List[Model]:
        params = {
            "model_slug": model_slug,
            "includes": includes,
            "owner": owner,
            "sort": sort,
            "featured": featured,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/models", params=params)
        resp.raise_for_status()

        return ModelQueryResult(**resp.json()).models
