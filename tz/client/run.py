from typing import TYPE_CHECKING, List, Optional

import pandas as pd

from tz.client import api, factory
from tz.client.api import schemas

if TYPE_CHECKING:
    from tz.client.model import Model
    from tz.client.scenario import Scenario


class ResultsCollection(pd.DataFrame):
    """
    A ResultsCollection is an extention of a Pandas DataFrame.

    It can be used in precisely the same way as a Pandas DataFrame
    but has a few extra useful constructors.
    """

    @property
    def _constructor(self):
        return ResultsCollection


class RunResults(schemas.PydanticBaseModel):
    id: str
    _node_capacity: Optional[ResultsCollection] = None
    _edge_capacity: Optional[ResultsCollection] = None
    _production: Optional[ResultsCollection] = None
    _flow: Optional[ResultsCollection] = None

    def _structure_series(self, series, node_id, tech_type, commodity=None) -> list:
        series_data = []
        for year, value in zip(series.x, series.y):
            entry = {
                "node_id": node_id,
                "technology_type": tech_type,
                "timestamp": pd.to_datetime(year, format="%Y"),
                "value": value,
            }
            if commodity:
                entry["commodity"] = commodity
            series_data.append(entry)
        return series_data

    def _structure_response(self, data: dict, commodity_column: bool = False) -> list:
        restructured_data = []
        for node_id, tech_data in data.items():
            for tech_type, series_data in tech_data.items():
                if commodity_column:
                    for commodity, series in series_data.items():
                        series_data = self._structure_series(series, node_id, tech_type, commodity)
                        restructured_data += series_data
                else:
                    series_data = self._structure_series(series_data, node_id, tech_type)
                    restructured_data += series_data
        return restructured_data

    def _structure_production_records(self, data: dict) -> list:
        records = [
            {"node": node, "technology": tech, "commodity": commodity, "year": year, "value": value}
            for node, techs in data.items()
            for tech, commodities in techs.items()
            for commodity, values in commodities.items()
            for year in values.x
            for value in values.y
        ]
        return records

    def _structure_flow_records(self, data: dict) -> list:
        records = [
            {
                "source_node": node1,
                "target_node": node2,
                "commodity": commodity,
                "flow_type": flow_type,
                "year": year,
                "value": value,
            }
            for node1, node2s in data.items()
            for node2, commodities in node2s.items()
            for commodity, flow_types in commodities.items()
            for flow_type, records in flow_types.items()
            for year in records.x
            for value in records.y
        ]
        return records

    @property
    def node_capacity(self) -> Optional[ResultsCollection]:
        if self._node_capacity is None:
            response = api.runs.get_chart_data(
                fullslug=self.id,
                attribute="node_capacity",
                chart_type="Capacity",
                node_or_edge="node",
            )
            if response.data is not None:
                self._node_capacity = ResultsCollection(self._structure_response(response.data))
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
            if response.data is not None:
                self._edge_capacity = ResultsCollection(
                    self._structure_response(response.data, commodity_column=True)
                )
                self._edge_capacity._table = "edge_capacity"
        return self._edge_capacity

    @property
    def production(self) -> Optional[ResultsCollection]:
        if self._production is None:
            response = api.runs.get_chart_data(
                fullslug=self.id,
                attribute="production_timeseries",
                chart_type="Production",
                node_or_edge="node",
            )
            if response.data is not None:
                self._production = ResultsCollection(
                    self._structure_production_records(response.data)
                )
                self._production._table = "production_timeseries"
        return self._production

    @property
    def flow(self) -> Optional[ResultsCollection]:
        if self._flow is None:
            response = api.runs.get_chart_data(
                fullslug=self.id,
                attribute="flow_timeseries",
                chart_type="Flow",
                node_or_edge="edge",
            )
            if response.data is not None:
                self._flow = ResultsCollection(self._structure_flow_records(response.data))
                self._flow._table = "flow_timeseries"
        return self._flow


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
