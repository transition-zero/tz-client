from typing import TYPE_CHECKING, List, Optional

import pandas as pd

from feo.client import api, factory
from feo.client.api import schemas

if TYPE_CHECKING:
    from feo.client.model import Model
    from feo.client.scenario import Scenario


class ResultsFilter(schemas.PydanticBaseModel):
    node_ids: List[str] | str | None = None
    edge_ids: List[str] | str | None = None


class ResultsCollection(pd.DataFrame):
    _filters: ResultsFilter | None = None
    _chart_type: str
    _chart_subtype: str | None

    @property
    def _constructor(self):
        return ResultsCollection

    @property
    def _constructor_sliced(self):
        return ResultsCollectionRow

    def filter(
        self,
        node_ids: List[str] | str | None = None,
        edge_ids: List[str] | str | None = None,
    ):
        self._filters = ResultsFilter(node_ids=node_ids, edge_ids=edge_ids)

    def next_page():
        pass


class ResultsCollectionRow(pd.Series):
    @property
    def _constructor(self):
        return ResultsCollectionRow

    @property
    def _constructor_expanddim(self):
        return ResultsCollection


class RunResults(schemas.PydanticBaseModel):
    id: str
    _node_capacity: ResultsCollection | None = None
    _edge_capacity: ResultsCollection | None = None
    _production: ResultsCollection | None = None
    _flow: ResultsCollection | None = None

    @property
    def node_capacity(self):
        if self._node_capacity is None:
            self._node_capacity = ResultsCollection()
            self._node_capacity._table = "node_capacity"
            return self._node_capacity
        return self._node_capacity

    @property
    def edge_capacity(self):
        if self._edge_capacity is None:
            self._edge_capacity = ResultsCollection()
            self._edge_capacity._table = "edge_capacity"
            return self._edge_capacity
        return self._edge_capacity

    @property
    def production(self):
        if self._production is None:
            self._production = ResultsCollection()
            self._production._table = "production"
            return self._production
        return self._production

    @property
    def flow(self):
        if self._flow is None:
            self._flow = ResultsCollection()
            self._flow._table = "flow"
            return self._flow
        return self._flow

    @property
    def price(self):
        if self._price is None:
            self._price = ResultsCollection()
            self._price._table = "price"
            return self._price
        return self._price


class Run(schemas.RunBase):
    _run_results: RunResults | None = None

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
            limit (int): The maximum number of search results to return per page.
            page (int): The page number of search results to return.

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
    def model(self) -> Optional["Model"]:
        """The model associated with this run."""
        run_data = api.runs.get(fullslug=self.id, includes="model")
        if run_data.model is None:
            return None
        return factory.model(**run_data.model.model_dump())

    @property
    def scenario(self) -> Optional["Scenario"]:
        """The scenario associated with this run."""
        run_data = api.runs.get(fullslug=self.id, includes="scenario")
        if run_data.scenario is None:
            return None
        return factory.scenario(**run_data.scenario.model_dump())

    @property
    def results(self):
        if self._run_results is None:
            self._run_results = RunResults(id=self.id)
            return self._run_results
        return self._run_results
