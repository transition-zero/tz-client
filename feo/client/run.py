from typing import TYPE_CHECKING, List, Optional, Union

import pandas as pd

import pandas as pd

import pandas as pd

from feo.client import api, factory
from feo.client.api import schemas

if TYPE_CHECKING:
    from feo.client.model import Model
    from feo.client.scenario import Scenario


class ResultsFilter(schemas.PydanticBaseModel):
    node_ids: Optional[Union[List[str], str]] = None
    edge_ids: Optional[Union[List[str], str]] = None


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
        edge_ids: Optional[List[str]] = None,
    ) -> None:
        self._filters = ResultsFilter(node_ids=node_ids, edge_ids=edge_ids)

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

    def to_feo_results(self) -> List[Result]:
        """Instantiate a list of Results from a ResultsCollection."""
        return [Result(**row) for idx, row in self.iterrows()]


class ResultsCollectionRow(pd.Series):
    @property
    def _constructor(self) -> "ResultsCollectionRow":
        return ResultsCollectionRow

    @property
    def _constructor_expanddim(self) -> "ResultsCollection":
        return ResultsCollection

    def to_feo_results(self) -> Result:
        return Result(
            **self.to_dict(),
        )


class RunResults(schemas.PydanticBaseModel):
    id: str
    _capacity: Optional[ResultsCollection] = None
    _production: Optional[ResultsCollection] = None
    _flow: Optional[ResultsCollection] = None
    _price: Optional[ResultsCollection] = None

    @property
    def capacity(self) -> Optional[ResultsCollection]:
        if self._capacity is None:
            run_response = api.runs.get(fullslug=self.id, includes="capacity")
            if hasattr(run_response, "capacity"):
                self._capacity = ResultsCollection().from_dict(run_response.capacity)
                self._capacity._table = "capacity"
            else:
                print("Capacity not found.")
                return None
        return self._capacity

    @property
    def production(self) -> Optional[ResultsCollection]:
        if self._production is None:
            run_response = api.runs.get(fullslug=self.id, includes="production")
            if hasattr(run_response, "production"):
                self._production = ResultsCollection().from_dict(run_response.production)
                self._production._table = "production"
            else:
                print("Production not found.")
                return None
        return self._production

    @property
    def flow(self) -> Optional[ResultsCollection]:
        if self._flow is None:
            run_response = api.runs.get(fullslug=self.id, includes="flow")
            if hasattr(run_response, "flow"):
                self._flow = ResultsCollection().from_dict(run_response.flow)
                self._flow._table = "flow"
            else:
                print("Flow not found.")
                return None
        return self._flow

    @property
    def price(self) -> Optional[ResultsCollection]:
        if self._price is None:
            run_response = api.runs.get(fullslug=self.id, includes="price")
            if hasattr(run_response, "price"):
                self._price = ResultsCollection().from_dict(run_response.price)
                self._price._table = "price"
            else:
                print("Price not found.")
                return None
        return self._price


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
    @property
    def results(self):
        if self._run_results is None:
            self._run_results = RunResults(id=self.id)
            return self._run_results
        return self._run_results
