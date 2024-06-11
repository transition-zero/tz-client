from datetime import datetime
from typing import List

from tz.client.api.base import BaseAPI
from tz.client.api.constants import CHART_TYPES
# fmt: off
from tz.client.api.generated_schema import (DeleteResponse, Run, RunCreate,
                                            RunPagination)
from tz.client.api.schemas import ChartData
from tz.client.api.utils import non_empty


class RunAPI(BaseAPI):
    def get(
        self,
        owner: str,
        model_slug: str,
        model_scenario_slug: str,
        run_slug: str,
        includes: str | None = None,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> Run:
        params = {
            "includes": includes,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }

        resp = self.client.get(
            f"/runs/{owner}:{model_slug}:{model_scenario_slug}:{run_slug}", params=params
        )
        resp.raise_for_status()

        return Run(**resp.json())

    def create(self, run: RunCreate) -> Run:
        resp = self.client.post("/runs", json=run.model_dump())
        resp.raise_for_status()
        return Run(**resp.json())

    def delete(
        self, owner: str, model_slug: str, model_scenario_slug: str, slug: str
    ) -> DeleteResponse:
        resp = self.client.delete(f"/runs/{owner}:{model_slug}:{model_scenario_slug}:{slug}")
        resp.raise_for_status()
        return DeleteResponse(**resp.json())

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
        params = {
            "fullslug": fullslug,
            "chart_type": chart_type,
            "capacity_type": capacity_type,
        }
        if node_or_edge == "node":
            params["node_ids"] = "*"
        elif node_or_edge == "edge":
            params["edge_ids"] = "*"
        elif chart_type in ["Production", "Capacity", "Flow"]:
            print("node_or_edge must be given as either 'node' or 'edge' for this chart type!")

        if year:
            params["year"] = str(year)

        resp = self.client.get(f"/runs/{fullslug}/chart_data", params=params)
        resp.raise_for_status()
        chart_data_response = ChartData(**resp.json())
        return getattr(chart_data_response, attribute)

    def search(
        self,
        slug: str | None = None,
        model_slug: str | None = None,
        model_scenario_slug: str | None = None,
        owner: str | None = None,
        featured: bool | None = None,
        includes: str | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> List[Run]:
        params = {
            "slug": slug,
            "model_slug": model_slug,
            "model_scenario_slug": model_scenario_slug,
            "owner": owner,
            "featured": featured,
            "includes": includes,
            "public": public,
            "limit": limit,
            "page": page,
        }

        resp = self.client.get("/runs", params=non_empty(params))
        resp.raise_for_status()
        r = RunPagination(**resp.json())
        if r.runs:
            return r.runs
        else:
            return []
