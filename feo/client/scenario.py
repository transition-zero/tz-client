from typing import List

from feo.client import api
from feo.client.api import schemas


class Scenario(schemas.Scenario):
    @classmethod
    def from_id(cls, id: str) -> "Scenario":
        """
        Initialize the Scenario object from an ID.

        Args:
            id (str): A scenario ID, e.g. `model-slug:scenario-slug`.

        Returns:
            Scenario: A Scenario object.
        """
        scenario = api.scenarios.get(fullslug=id)
        return cls(**scenario.model_dump())

    @classmethod
    def search(
        cls,
        scenario_slug: str | None = None,
        model_slug: str | None = None,
        includes: str | None = None,
        owner_id: str | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> List["Scenario"]:
        """
        Search for scenarios based on various filters.

        Args:
            scenario_slug (str | None): The slug of the scenario to search for.
            model_slug (str | None): The slug of the model to filter scenarios by.
            includes (str | None): Related resources to be included in the search result.
            owner_id (str | None): The ID of the owner to filter scenarios by.
            featured (bool | None): Whether to filter scenarios by featured status.
            public (bool | None): Whether to filter scenarios by public status.
            limit (int): The maximum number of scenarios to return (default is 5).
            page (int): The page number of the search results (default is 0).

        Returns:
            List[Scenario]: A list of Scenario objects matching the search criteria.
        """

        search_results = api.scenarios.search(
            scenario_slug=scenario_slug,
            model_slug=model_slug,
            includes=includes,
            owner_id=owner_id,
            featured=featured,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**scenario.model_dump()) for scenario in search_results]

    @property
    def id(self) -> str:
        """
        The ID of the scenario. A combination of the model slug and scenario slug.
        """
        return f"{self.model_slug}:{self.slug}"
