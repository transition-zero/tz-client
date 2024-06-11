from typing import List, Optional

from tz.client import api
from tz.client.api import generated_schema
from tz.client.utils import lazy_load_single_relationship


class ModelScenario(generated_schema.ModelScenario):
    # Lazy-loaded
    _model: Optional["Model"] = None  # type: ignore[name-defined] # noqa: F821
    _featured_run: Optional["Run"] = None  # type: ignore[name-defined] # noqa: F821

    @classmethod
    def from_fullslug(cls, fullslug: str) -> "ModelScenario":
        """
        Load the ModelScenario from a compound slug composed of:

            {owner_username}:{model_slug}:{model_scenario_slug}

        Returns:
            ModelScenario: A ModelScenario object.
        """
        parts = fullslug.split(":")
        if len(parts) != 3:
            raise Exception(
                f"""Need 3 components for 'fullslug' for 'ModelScenario':
                {fullslug}, found {len(parts)}."""
            )
        return cls.from_slug(owner=parts[0], model_slug=parts[1], model_scenario_slug=parts[2])

    @classmethod
    def from_slug(cls, owner: str, model_slug: str, model_scenario_slug: str) -> "ModelScenario":
        """
        Initialize the Scenario object from the slugs.

        Args:
            owner (str): The username of the owner
            model_slug (str): A model slug
            model_scenario_slug (str): A model scenario slug

        Returns:
            ModelScenario: A ModelScenario object.
        """
        scenario = api.model_scenarios.get(
            owner=owner, model_slug=model_slug, model_scenario_slug=model_scenario_slug
        )
        c = cls(**scenario.model_dump())
        return c

    @classmethod
    def delete(cls, owner: str, model_slug: str, slug: str) -> generated_schema.DeleteResponse:
        result = api.model_scenarios.delete(owner=owner, model_slug=slug, slug=slug)
        return generated_schema.DeleteResponse(**result.model_dump())

    @classmethod
    def create(cls, model_scenario: generated_schema.ModelScenarioCreate) -> "ModelScenario":
        result = api.model_scenarios.create(model_scenario)
        return cls(**result.model_dump())

    @classmethod
    def search(
        cls,
        model_scenario_slug: str | None = None,
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
            model_scenario_slug (str | None): The slug of the scenario to search for.
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

        search_results = api.model_scenarios.search(
            model_scenario_slug=model_scenario_slug,
            model_slug=model_slug,
            includes=includes,
            owner_id=owner_id,
            featured=featured,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**scenario.model_dump()) for scenario in search_results]

    # @property
    # def runs(self) -> list["Run"]:
    #     """The featured run associated with this scenario."""
    #     scenario_data = api.scenarios.get(fullslug=self.id, includes="runs")
    #     if scenario_data.runs is None:
    #         return []
    #     return [factory.run(**r.model_dump()) for r in scenario_data.runs]

    def __str__(self) -> str:
        return f"ModelScenario: {self.name} (fullslug={self.fullslug})"


lazy_load_single_relationship(
    ModelScenario,
    "Model",
    "model",
    lambda self, ctx: api.model_scenarios.get(
        owner=self.owner,
        model_slug=ctx["model"].split(":")[1],
        model_scenario_slug=self.slug,
        includes="model",
    ),
)

lazy_load_single_relationship(
    ModelScenario,
    "Run",
    "featured_run",
    lambda self, ctx: api.model_scenarios.get(
        owner=self.owner,
        model_slug=ctx["model"].split(":")[1],
        model_scenario_slug=self.slug,
        includes="featured_run",
    ),
)
