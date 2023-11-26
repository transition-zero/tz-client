from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Publisher, PublisherQueryResponse


class PublisherAPI(BaseAPI):
    def get(self, slug: str) -> Publisher:
        resp = self.client.get(f"/publishers/{slug}")
        resp.raise_for_status()

        return Publisher(**resp.json())

    def search(
        self,
        name: str | None = None,
        short_name: str | None = None,
        url: str | None = None,
        public: bool | None = None,
        organisation_type: str | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> List[Publisher]:
        params = {
            "name": name,
            "short_name": short_name,
            "url": url,
            "public": public,
            "organisation_type": organisation_type,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/publishers", params=params)
        resp.raise_for_status()

        return PublisherQueryResponse(**resp.json()).publishers
