# mypy: ignore-errors
from typing import List, Optional

import pandas as pd

from tz.client import api
from tz.client.api import generated_schema, schemas
from tz.client.utils import lazy_load_single_relationship


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


class Run(generated_schema.Run):
    # _run_results: Optional[RunResults] = None
    _model_scenario: Optional["ModelScenario"] = None  # type: ignore[name-defined] # noqa: F821

    @classmethod
    def from_fullslug(cls, fullslug: str) -> "Run":
        """
        Load the Run from a compound slug composed of:

            {owner_username}:{model_slug}:{model_scenario_slug}:{run_slug}

        Returns:
            Run: A Run object.
        """
        parts = fullslug.split(":")
        if len(parts) != 4:
            raise Exception(
                f"Need 4 components for 'fullslug' for 'Run': {fullslug}, found {len(parts)}."
            )
        return cls.from_slug(
            owner=parts[0], model_slug=parts[1], model_scenario_slug=parts[2], run_slug=parts[3]
        )

    @classmethod
    def from_slug(
        cls, owner: str, model_slug: str, model_scenario_slug: str, run_slug: str
    ) -> "Run":
        """
        Initialize the Run object from the relevant slugs.

        Args:
            owner (str): The username of the owner
            model_slug (str): The model slug
            model_scenario_slug (str): The model scenario slug
            run_slug (str): The run slug

        Returns:
            Run: A Run object.
        """
        run_reponse = api.runs.get(
            owner=owner,
            model_slug=model_slug,
            model_scenario_slug=model_scenario_slug,
            run_slug=run_slug,
        )
        return cls(**run_reponse.model_dump())

    @classmethod
    def search(
        cls,
        slug: Optional[str] = None,
        model_slug: Optional[str] = None,
        model_scenario_slug: Optional[str] = None,
        owner: Optional[str] = None,
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
            owner (str, optional): The username of the owner.
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
            model_scenario_slug=model_scenario_slug,
            owner_id=owner,  # TODO: Fix once the owner id problem is resolved
            featured=featured,
            includes=includes,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**r.model_dump()) for r in search_results]

    @property
    def fullslug(self) -> str:
        """The full slug of the run. A combination of the owner username,
        and model, model scenario, and run slugs."""
        return (
            f"{self.owner}:{self.model_scenario.model.slug}:{self.model_scenario.slug}:{self.slug}"
        )

    # TODO: Implement this later
    # @property
    # def results(self) -> RunResults:
    #     if self._run_results is None:
    #         self._run_results = RunResults(id=self.id)
    #         return self._run_results
    #     return self._run_results

    def __str__(self) -> str:
        return f"Run: {self.name} (fullslug={self.fullslug})"


def _load_model_scenario(self, ctx):
    owner, model_slug, model_scenario_slug = ctx["model_scenario"].split(":")
    r = api.runs.get(
        owner=owner,
        model_slug=model_slug,
        model_scenario_slug=model_scenario_slug,
        run_slug=self.slug,
        includes="model_scenario",
    )
    return r


lazy_load_single_relationship(Run, "ModelScenario", "model_scenario", _load_model_scenario)
