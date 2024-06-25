from typing import List

from tz.client.api.base import BaseAPI
# fmt: off
from tz.client.api.generated_schema import (DeleteResponse, Model, ModelCreate,
                                            ModelPagination)
from tz.client.api.utils import non_empty


class ModelAPI(BaseAPI):
    def get(self, model_slug: str, owner: str, includes: str | None = None) -> Model:
        resp = self.client.get(f"/models/{owner}:{model_slug}", params={"includes": includes})
        resp.raise_for_status()

        return Model(**resp.json())

    def create(self, model: ModelCreate) -> Model:
        resp = self.client.post("/models", json=model.model_dump())
        resp.raise_for_status()
        return Model(**resp.json())

    def delete(self, owner: str, slug: str) -> DeleteResponse:
        resp = self.client.delete(f"/models/{owner}:{slug}")
        resp.raise_for_status()
        return DeleteResponse(**resp.json())

    def search(
        self,
        slug: str | None = None,
        includes: str | None = None,
        owner: str | None = None,
        sort: str | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> List[Model]:
        params = {
            "slug": slug,
            "includes": includes,
            "owner": owner,
            "sort": sort,
            "featured": featured,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/models", params=non_empty(params))
        resp.raise_for_status()

        r = ModelPagination(**resp.json())
        if r.models is None:
            return []
        return r.models
