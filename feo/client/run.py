from typing import TYPE_CHECKING, List

from feo.client import api
from feo.client.api import schemas

if TYPE_CHECKING:
    from feo.client.model import Model
    from feo.client.scenario import Scenario


class Run(schemas.RunBase):
    @classmethod
    def from_id(cls, id: str) -> "Run":
        """
        Initialize the Run object from an ID.

        Args:
            id (str): A run ID, e.g. `model-slug:scenario-slug:run-slug`.

        Returns:
            Run: A Run object.
        """
        run = api.runs.get(fullslug=id)
        return cls(**run.model_dump())

    @classmethod
    def search(
        cls,
        slug: str | None = None,
        model_slug: str | None = None,
        scenario_slug: str | None = None,
        owner_id: str | None = None,
        featured: bool | None = None,
        includes: str | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> List["Run"]:
        """
        Search for runs using various filters.

        Args:
            slug (str, optional): The slug of the run.
            model_slug (str, optional): The slug of the model to filter by.
            scenario_slug (str, optional): The slug of the scenario to filter by.
            owner_id (str, optional): The ID of the owner.
            featured (bool, optional): Filter by whether the run is featured.
            includes (str, optional): Additional fields to include in the search results.
            public (bool, optional): Filter by whether the run is public.
            limit (int, optional): The maximum number of runs to return. Default is 5.
            page (int, optional): The page number of the results. Default is 0.

        Returns:
            List[Run]: A list of Run objects.
        """

        search_results = api.runs.search(
            slug=slug,
            model_slug=model_slug,
            scenario_slug=scenario_slug,
            owner_id=owner_id,
            featured=featured,
            includes=includes,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**run.model_dump()) for run in search_results]

    @property
    def id(self) -> str:
        """The ID of the run. A combination of the model, scenario, and run slugs."""
        return f"{self.model_slug}:{self.scenario_slug}:{self.slug}"

    @property
    def model(self) -> "Model":
        """The model associated with this run."""
        from feo.client.model import Model

        scenario_data = api.models.get(slug=self.id, includes="model")
        return Model(**scenario_data.model.model_dump())

    @property
    def scenario(self) -> "Scenario":
        """The scenario associated with this run."""
        from feo.client.scenario import Scenario

        scenario_data = api.scenarios.get(slug=self.id, includes="scenario")
        return Scenario(**scenario_data.scenario.model_dump())
