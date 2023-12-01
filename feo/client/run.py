from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union

import pandas as pd

from feo.client import api, factory
from feo.client.api import schemas

if TYPE_CHECKING:
    from feo.client.model import Model
    from feo.client.scenario import Scenario


class ResultsFilter(schemas.PydanticBaseModel):
    node_ids: Optional[Union[List[str], str]] = None
    edge_ids: Optional[Union[List[str], str]] = None
    technology: Optional[str] = None
    commodity: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Result(schemas.ResultBase):
    pass


class ResultsCollection(pd.DataFrame):
    """A ResultsCollection is an extention of a Pandas DataFrame.

    It can be used in precisely the same way as a Pandas DataFrame
    but has a few extra useful constructors.

    Args:
        _filters Optional[List[Result]]: stores the filters currently applied to the df
        _scope Optional[schemas.CollectionScope]: params for generating api query for pagination
        _page Optional[int]: if generated from an API query, the current page of the query.
        _chart_type str: stores the type of the df
        _chart_subtype Optional[str]: stores the subtype of the df
    """

    _filters: List[Result] | None = None
    _scope: Optional[schemas.CollectionScope] = None
    _page: int | None = None
    _chart_type: str
    _chart_subtype: str | None

    @property
    def _constructor(self) -> "ResultsCollection":
        return ResultsCollection

    @property
    def _constructor_sliced(self) -> "ResultsCollectionRow":
        return ResultsCollectionRow

    def from_feo_results(cls, results: List[Result]) -> "ResultsCollection":
        """Instiate an ResultsCollection from a list of results."""
        # pd.DataFrame.from_records
        return cls.from_records([r.model_dump() for r in results])

    def filter(
        self,
        node_id: Optional[str] = None,
        node_ids: Optional[List[str]] = None,
        edge_id: Optional[str] = None,
        edge_ids: Optional[List[str]] = None,
    ) -> None:
        if node_ids is None and node_id is not None:
            node_ids = [node_id]
        if edge_ids is None and edge_id is not None:
            edge_ids = [edge_id]
        self._filters = ResultsFilter()

    def next_page(self) -> int:
        """
        Paginate through results. The Result collection must have a `_scope`.
        Returns the next page of results and concatenates them in-place to the current collection.
        """
        if not self._scope:
            raise ValueError("Cant iterate an unscoped ResultsCollection")
        new_collection = self.__class__.from_feo_results(
            api.results.get(parent_node_id=self._scope.parent_node_id, page=self._page + 1)
        )
        self._page += 1

        self.__dict__.update(pd.concat([self, new_collection], ignore_index=True).__dict__)
        return len(new_collection)


class ResultsCollectionRow(pd.Series):
    @property
    def _constructor(self) -> "ResultsCollectionRow":
        return ResultsCollectionRow

    @property
    def _constructor_expanddim(self) -> "ResultsCollection":
        return ResultsCollection


class RunResults(schemas.PydanticBaseModel):
    id: str
    _node_capacity: Optional[ResultsCollection] = None
    _edge_capacity: Optional[ResultsCollection] = None
    _production: Optional[ResultsCollection] = None
    _node_flow: Optional[ResultsCollection] = None
    _edge_flow: Optional[ResultsCollection] = None

    @property
    def node_capacity(self) -> Optional[ResultsCollection]:
        if self._node_capacity is None:
            response = api.runs.get_chart_data(
                fullslug=self.id,
                attribute="node_capacity",
                chart_type="Capacity",
                node_or_edge="node",
            )
            self._node_capacity = ResultsCollection().from_dict(response.data)
            self._node_capacity._table = "node_capacity"
        return self._node_capacity

    @property
    def edge_capacity(self) -> Optional[ResultsCollection]:
        if self._edge_capacity is None:
            response = api.runs.get_chart_data(
                fullslug=self.id,
                attribute="edge_capacity",
                chart_type="Capacity",
                node_or_edge="edge",
            )
            self._edge_capacity = ResultsCollection().from_dict(response.data)
            self._edge_capacity._table = "edge_capacity"
        return self._edge_capacity

    @property
    def production(self) -> Optional[ResultsCollection]:
        if self._production is None:
            response = api.runs.get_chart_data(
                fullslug=self.id, chart_type="AggregateProductionBar"
            )
            if hasattr(response, "production"):
                self._production = ResultsCollection().from_dict(response.data)
                self._production._table = "production"
            else:
                print("Production not found.")
                return None
        return self._production

    @property
    def node_flow(self) -> Optional[ResultsCollection]:
        if self._node_flow is None:
            response = api.runs.get(fullslug=self.id, includes="flow")
            if hasattr(response, "flow"):
                self._node_flow = ResultsCollection().from_dict(response.flow)
                self._node_flow._table = "flow"
            else:
                print("Flow not found.")
                return None
        return self._node_flow

    @property
    def edge_flow(self) -> Optional[ResultsCollection]:
        if self._edge_flow is None:
            response = api.runs.get(fullslug=self.id, includes="flow")
            if hasattr(response, "flow"):
                self._edge_flow = ResultsCollection().from_dict(response.flow)
                self._edge_flow._table = "flow"
            else:
                print("Flow not found.")
                return None
        return self._edge_flow


class Run(schemas.RunBase):
    _run_results: Optional[RunResults] = None

    @classmethod
    def from_id(cls, id: str) -> "Run":
        """
        Initialize the Run object from an ID.

        Args:
            id (str): A run ID, e.g. `model-slug:scenario-slug:run-slug`.

        Returns:
            Run: A Run object.
        """
        run_reponse = api.runs.get(fullslug=id)
        return cls(**run_reponse.model_dump())

    @classmethod
    def search(
        cls,
        slug: Optional[str] = None,
        model_slug: Optional[str] = None,
        scenario_slug: Optional[str] = None,
        owner_id: Optional[str] = None,
        featured: Optional[bool] = None,
        includes: Optional[str] = None,
        public: Optional[bool] = None,
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

        return [cls(**r.model_dump()) for r in search_results]

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
    def results(self) -> RunResults:
        if self._run_results is None:
            self._run_results = RunResults(id=self.id)
            return self._run_results
        return self._run_results

    def __str__(self) -> str:
        return f"Run: {self.name} (id={self.id})"
