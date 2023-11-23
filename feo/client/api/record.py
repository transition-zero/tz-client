from typing import List, Union

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Record, RecordResponse


class RecordAPI(BaseAPI):
    base_url = "/records"

    def get(
        self,
        ids: Union[str, List[str]],
        includes: Union[str, None] = None,
    ) -> List[Record]:
        params = dict(
            includes=includes,
        )

        if isinstance(ids, list):
            ids = ",".join(ids)

        resp = self.client.get(f"{self.base_url}/{ids}", params=params)
        resp.raise_for_status()

        return RecordResponse(**resp.json()).records


class LanduseReductionsAPI(RecordAPI):
    base_url = "/records/landuse-reductions"
