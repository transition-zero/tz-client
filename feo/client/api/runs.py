from datetime import datetime
from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.constants import CHART_TYPES
from feo.client.api.schemas import ChartData, Run, RunQueryResult


class RunAPI(BaseAPI):
    def get(
        self,
        fullslug: str,
        includes: str | None = None,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> Run:
        params = {
            "fullslug": fullslug,
            "includes": includes,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }

        resp = self.client.get(f"/runs/{fullslug}", params=params)
        resp.raise_for_status()

        return Run(**resp.json())

    def get_chart_data(
        self,
        fullslug: str,
        attribute: str,
        chart_type: str,
        capacity_type: str = "gross",
        node_or_edge: str | None = None,
        year: int | None = None,
    ) -> Run:
        if chart_type not in CHART_TYPES:
            print(f"chart_type {chart_type} invalid- must be one of {CHART_TYPES}")
        params = {"fullslug": fullslug, "chart_type": chart_type, "capacity_type": capacity_type}
        if node_or_edge == "node":
            params["node_ids"] = "*"
        elif node_or_edge == "edge":
            params["edge_ids"] = "*"
        elif chart_type in ["Production", "Capacity", "Flow"]:
            print("node_or_edge must be given as either 'node' or 'edge' for this chart type!")

        if year:
            params["year"] = year

        resp = self.client.get(f"/runs/{fullslug}/chart_data", params=params)
        resp.raise_for_status()
        chart_data_response = ChartData(**resp.json())
        return getattr(chart_data_response, attribute)

    def search(
        self,
        slug: str | None = None,
        model_slug: str | None = None,
        scenario_slug: str | None = None,
        owner_id: str | None = None,
        featured: bool | None = None,
        includes: str | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> List[Run]:
        params = {
            "slug": slug,
            "model_slug": model_slug,
            "scenario_slug": scenario_slug,
            "owner_id": owner_id,
            "featured": featured,
            "includes": includes,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/runs", params=params)
        resp.raise_for_status()

        return RunQueryResult(**resp.json()).runs
