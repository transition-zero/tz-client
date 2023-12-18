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
        source_slug: str | None = None,
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
            source_slug (str, optional): The slug of the source.
            l_abbrv (str, optional): The abbreviation of the license.
            publisher_slug (str, optional): The slug of the publisher.
            links (list, optional): The links of the source.
            license (dict, optional): The license of the source.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.HTTPError: If the API request fails.
            TypeError: If any of the arguments are not of the correct type.
        """

        # Check types
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(short_name, str):
            raise TypeError("short_name must be a string")
        if not isinstance(public, bool):
            raise TypeError("public must be a boolean")
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        if year is not None and not isinstance(year, int):
            raise TypeError("year must be an integer or None")
        if month is not None and not isinstance(month, int):
            raise TypeError("month must be an integer or None")
        if day is not None and not isinstance(day, int):
            raise TypeError("day must be an integer or None")
        if quarter is not None and not isinstance(quarter, int):
            raise TypeError("quarter must be an integer or None")
        if license_abbrv is not None and not isinstance(license_abbrv, str):
            raise TypeError("license_abbrv must be a string or None")
        if publisher_slug is not None and not isinstance(publisher_slug, str):
            raise TypeError("publisher_slug must be a string or None")
        if source_slug is not None and not isinstance(source_slug, str):
            raise TypeError("source_slug must be a string or None")
        if links is not None and not isinstance(links, list):
            raise TypeError("links must be a list or None")
        if nodes is not None and not isinstance(nodes, list):
            raise TypeError("nodes must be a list or None")
        if license is not None and not isinstance(license, str):
            raise TypeError("license must be a string or None")

        source_data = {
            "name": name,
            "short_name": short_name,
            "public": public,
            "year": year,
            "month": month,
            "day": day,
            "quarter": quarter,
            "description": description,
            "license_abbrv": license_abbrv,
            "publisher_slug": publisher_slug,
            "slug": source_slug,
            "links": links,
            "nodes": nodes,
            "license": license,
        }

        resp = self.client.post("/sources", json=source_data)
        resp.raise_for_status()
        return resp.json()
