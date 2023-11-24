from typing import List

from pydantic import root_validator

from feo.client import api
from feo.client.api import schemas


class Scenario(schemas.Scenario):
    def __init__(self, fullslug: str, **kwargs):
        """Initialise Scenario from `fullslug` as a positional argument"""
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
        Search for nodes using an alias.

        Args:
            alias (str): The target alias to search.
            threshold (float): The desired confidence in the search result.
            node_type (str): filter search to a specific node type.
            sector (str): the industrial sector to filter scenarios for

        Returns:
            List[Scenario]: A list of Scenario objects.
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
