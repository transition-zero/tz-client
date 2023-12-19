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

    def _post(
        self,
        name: str,
        short_name: str,
        public: bool,
        description: str,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        quarter: int | None = None,
        license_abbrv: str | None = None,
        publisher_slug: str | None = None,
        slug: str | None = None,
        links: list | None = None,
        nodes: list | None = None,
        license: str | None = None,
    ):
        """
        POST a new source to the API.

        Args:
            name (str): The name of the source.
            short_name (str): The short name of the source.
            public (bool): Indicates if the source is public or not.
            description (str): The description of the source.
            year (int, optional): The year of the source.
            month (int, optional): The month of the source.
            day (int, optional): The day of the source.
            quarter (int, optional): The quarter of the source.
            license_abbrv (str, optional): License for the source.
            publisher_slug (str, optional): The slug of the publisher for the source.
            slug (str, optional): The slug of the source.
            l_abbrv (str, optional): The abbreviation of the license.
            publisher_slug (str, optional): The slug of the publisher.
            links (list, optional): The links of the source.
            license (dict, optional): The license of the source.

        Returns:
            dict: The JSON response from the API.

        Raises:
            RefreshTokenError: If the refresh token is invalid.
            HTTPError: If the POST request fails. Note that if the
            error code is 401, this is likely due to invalid credentials.
        """

        source_data = {
            "name": name,
            "short_name": short_name,
            "public": public,
            "description": description,
            "year": year,
            "month": month,
            "day": day,
            "quarter": quarter,
            "license_abbrv": license_abbrv,
            "publisher_slug": publisher_slug,
            "slug": slug,
            "links": links,
            "nodes": nodes,
            "license": license,
        }

        resp = self.client.post("/sources", json=source_data)
        resp.raise_for_status()
        return resp.json()
