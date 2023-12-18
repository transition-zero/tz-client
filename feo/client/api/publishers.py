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

    def _post(
        self,
        name: str,
        short_name: str,
        organisation_type: str,
        url: str | None = None,
        public: bool | None = None,
        slug: str | None = None,
    ):
        """
        Sends a POST request to create a new publisher.

        Args:
            name (str): The name of the publisher.
            short_name (str): The short name of the publisher.
            organisation_type (str): The type of the organisation.
            url (str | None, optional): The URL of the publisher.
            public (bool | None, optional): Indicates if the publisher is public or not.
            slug (str | None, optional): The slug of the publisher.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.HTTPError: If the API request fails.
            TypeError: If any of the arguments are not of the correct type.
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(short_name, str):
            raise TypeError("short_name must be a string")
        if not isinstance(organisation_type, str):
            raise TypeError("organisation_type must be a string")
        if url is not None and not isinstance(url, str):
            raise TypeError("url must be a string or None")
        if public is not None and not isinstance(public, bool):
            raise TypeError("public must be boolean or None")
        if slug is not None and not isinstance(slug, str):
            raise TypeError("slug must be a string or None")

        publisher_data = {
            "name": name,
            "short_name": short_name,
            "url": url,
            "public": public,
            "organisation_type": organisation_type,
            "slug": slug,
        }
        resp = self.client.post("/publishers", json=publisher_data)
        resp.raise_for_status()
        return resp.json()
