import os
from typing import Optional

import httpx

from transitionzero.client.base import Base


class Model(Base):
    # from tz.client import Models, Data, Geog
    # Client.model.search_run

    def __init__(self):
        super().__init__()
        self.client = httpx.Client(
            base_url=os.environ.get(
                "FEO_MODEL_URL", "https://model-results.feo.transitionzero.org/"
            ),
            headers=self.headers,
        )

    def search_model_runs(
        self,
        model_id: Optional[str],
        scenario_id: Optional[str],
        owner: Optional[str],
        public: Optional[bool],
        limit: Optional[int],
        page: Optional[int],
    ):
        r = self.client.get(
            "v1/model_run/",
            params={
                "model_id": model_id,
                "scenario_id": scenario_id,
                "owner": owner,
                "public": public,
                "limit": limit,
                "page": page,
            },
        )

        self.catch_errors(r)

        return r.json()

    def get_model_run(self, uuid: str, includes: str):
        r = self.client.get(f"v1/model_run/{uuid}")

        self.catch_errors(r)

        return r.json()
