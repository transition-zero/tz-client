# mypy: ignore-errors
# TODO: ^ Bring back mypy when we're ready.

from typing import TYPE_CHECKING, List, Optional

from tz.client import api, factory
from tz.client.api import generated_schema

if TYPE_CHECKING:
    from tz.client.model import Model
    from tz.client.run import Run


class ModelScenario(generated_schema.ModelScenario):
    @classmethod
    def from_slug(cls, owner: str, model_slug: str, model_scenario_slug: str) -> "ModelScenario":
        """
        Initialize the Scenario object from the slugs.

        Args:
            id (str): A scenario ID, e.g. `model-slug:scenario-slug`.

        Returns:
            ModelScenario: A ModelScenario object.
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
    ) -> List["ModelScenario"]:
        """
        Search for scenarios based on various filters.

        Args:
            scenario_slug (str | None): The slug of the scenario to search for.
            model_slug (str | None): The slug of the model to filter scenarios by.
            includes (str | None): Related resources to be included in the search result.
            owner_id (str | None): The ID of the owner to filter scenarios by.
            featured (bool | None): Whether to filter scenarios by featured status.
            public (bool | None): Whether to filter scenarios by public status.
            limit (int): The maximum number of search results to return per page.
            page (int): The page number of search results to return.

        Returns:
            List[ModelScenario]: A list of Scenario objects matching the search criteria.
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

    @property
    def model(self) -> Optional["Model"]:
        """The model associated with this scenario."""
        scenario_data = api.scenarios.get(fullslug=self.id, includes="model")
        if scenario_data.model is None:
            return None
        return factory.model(**scenario_data.model.model_dump())

    @property
    def featured_run(self) -> Optional["Run"]:
        """The featured run associated with this scenario."""
        scenario_data = api.scenarios.get(fullslug=self.id, includes="featured_run")
        if scenario_data.featured_run is None:
            return None
        return factory.run(**scenario_data.featured_run.model_dump())

    @property
    def runs(self) -> list["Run"]:
        """The featured run associated with this scenario."""
        scenario_data = api.scenarios.get(fullslug=self.id, includes="runs")
        if scenario_data.runs is None:
            return []
        return [factory.run(**r.model_dump()) for r in scenario_data.runs]

    def __str__(self) -> str:
        return f"ModelScenario: {self.name} (id={self.id})"
