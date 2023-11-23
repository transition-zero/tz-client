from typing import List, Union

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Record, RedcordResponse


class RecordAPI(BaseAPI):
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

        resp = self.client.get(f"/records/{ids}", params=params)
        resp.raise_for_status()

        return RedcordResponse(**resp.json()).records
