from typing import List, Union

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Technology, TechnologyQueryResponse


class TechnologyAPI(BaseAPI):
    def get(
        self,
        slug: str,
        includes: Union[str, None] = None,
    ) -> Technology:
        params = dict(
            includes=includes,
        )
        resp = self.client.get(f"/technologies/{slug}", params=params)
        resp.raise_for_status()

        return Technology(**resp.json())

    def search(
        self,
        uuid: str | None = None,
        slug: str | None = None,
        name: str | None = None,
        owner_id: str | None = None,
        public: bool | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> List[Technology]:
        params = {
            "uuid": uuid,
            "slug": slug,
            "name": name,
            "owner_id": owner_id,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/technologies", params=params)
        resp.raise_for_status()

        return TechnologyQueryResponse(**resp.json()).technologies

    def post(
        self,
        name: str,
        slug: str,
        public: bool,
        properties: dict | None = None,
        parents: list[str] | None = None,
        children: list[str] | None = None,
    ):
        """
        POST a new technology to the API.

        Args:
            name (str): The name of the technology.
            slug (str): The slug of the technology.
            public (bool): Whether the technology is public or not.
            properties (dict, optional): Additional properties of the technology.
            parents (list[str], optional): The id of the parents of the technology.
            children (list[str], optional): The id of the children of the technology.

        Returns:
            dict: The JSON response from the API.

        Raises:
            RefreshTokenError: If the refresh token is invalid.
            HTTPError: If the POST request fails. Note that if the
            error code is 401, this is likely due to invalid credentials.
        """

        technology_data = {
            "name": name,
            "slug": slug,
            "public": public,
            "properties": properties,
            "parents": parents,
            "children": children,
        }
        resp = self.client.post("/technologies", json=technology_data)
        resp.raise_for_status()
        return resp.json()

    def delete(self, slug: str):
        """
        DELETE a technology via the API.

        Args:
            slug (str): The slug of the technology to delete.

        Raises:
            RefreshTokenError: If the refresh token is invalid.
            HTTPError: If the DELETE request fails. Note that if the
            error code is 401, this is likely due to invalid credentials.
        """
        resp = self.client.delete("/technologies", json={"slug": slug})
        resp.raise_for_status()
        return resp.json()
