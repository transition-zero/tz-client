from typing import List

from pydantic import root_validator

from feo.client import api
from feo.client.api import schemas


class Scenario(schemas.Scenario):
    def __init__(self, fullslug: str, **kwargs):
        """
        Initialise the Scenario object

        Args:
            fullslug (str): a combination of the model slug and scenario slug, separated
                by a colon, e.g. `model-slug:scenario-slug`
            **kwargs: Additional keyword arguments to be passed to the parent class.
        """
        super(self.__class__, self).__init__(fullslug=fullslug, **kwargs)

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
            model_slug (str | None): The slug of the model to search for.
            includes (str | None): The fields to include in the search results.
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

    @root_validator(pre=True)
    def maybe_initialise_from_api(cls, values):
        fullslug = values.get("fullslug")
        if fullslug is not None:
            # call from API
            scenario = api.scenarios.get(fullslug)

            for key, val in scenario.model_dump().items():
                values[key] = val

            return values

        return values
