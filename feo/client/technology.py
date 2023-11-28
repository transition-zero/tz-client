from typing import List

from feo.client import api
from feo.client.api import schemas


class Technology(schemas.Technology):
    @classmethod
    def from_id(cls, id: str) -> "Technology":
        """
        Initialize the Technology object from an ID.

        Args:
            id (str): A technology ID, e.g. `coal`.

        Returns:
            Technology: A Technology object.
        """
        technology = api.technologies.get(slug=id)
        return cls(**technology.model_dump())

    @classmethod
    def search(
        cls,
        uuid: str | None = None,
        slug: str | None = None,
        name: str | None = None,
        owner_id: str | None = None,
        public: bool | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> List["schemas.Technology"]:
        """
        Search for technologies.

        Args:
            uuid (str | None): The target technology UUID to search.
            slug (str | None): The target technology slug to search.
            names (str | None): The target technology name to search.
            owner_id (str | None): The owner of the technologiess to filter.
            public (bool | None): Filter technologies by public status.
            limit (int): The maximum number of search results to return.
            page (int): The page number of search results to return.

        Returns:
            List[Technology]: A list of Technology objects.
        """

        search_results = api.technologies.search(
            uuid=uuid,
            slug=slug,
            name=name,
            owner_id=owner_id,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**technology.model_dump()) for technology in search_results]

    @property
    def id(self) -> str:
        """The ID of the technology."""
        return self.slug
