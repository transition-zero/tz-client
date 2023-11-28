from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Source, SourceQueryResponse


class SourceAPI(BaseAPI):
    def get(self, slug: str, includes: str = "") -> Source:
        resp = self.client.get(f"/sources/{slug}", params=dict(includes=includes))
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
        publisher_slug: str | None = None,
        publisher_name: str | None = None,
        includes: str = "",
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
            "includes": includes,
        }

        resp = self.client.get("/sources", params=params)
        resp.raise_for_status()

        return SourceQueryResponse(**resp.json()).sources
