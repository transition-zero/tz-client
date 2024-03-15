from typing import List

from tz.client.api.base import BaseAPI
from tz.client.api.schemas import Publisher, PublisherQueryResponse


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

    def post(
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
            RefreshTokenError: If the refresh token is invalid.
            HTTPError: If the POST request fails. Note that if the
            error code is 401, this is likely due to invalid credentials.
        """

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
