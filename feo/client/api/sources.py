from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Source, SourceQueryResult


class SourceAPI(BaseAPI):
    def get(self, slug: str) -> Source:
        resp = self.client.get(f"/sources/{slug}")
        resp.raise_for_status()

        return Source(**resp.json())

    def search(
        self,
        public: bool = True,
        name: str | None = None,
        short_name: str | None = None,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        quarter: int | None = None,
        license: str | None = None,
        publisher_id: int | None = None,
        publisher_name: str | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> List[Source]:
        params = {
            "public": public,
            "name": name,
            "short_name": short_name,
            "year": year,
            "month": month,
            "day": day,
            "quarter": quarter,
            "license": license,
            "publisher_name": publisher_name,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/sources", params=params)
        resp.raise_for_status()

        return SourceQueryResult(**resp.json()).sources
