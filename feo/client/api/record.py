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

    def post(
        self,
        node_id: str,
        public: bool,
        source_id: int,
        timestamp: str,
        valid_timestamp_start: str,
        valid_timestamp_end: str,
        datum_type: str,
        datum_detail: str,
        value: float,
        unit: str,
        properties: dict,
    ) -> dict:
        params = dict(
            node_id=node_id,
            public=public,
            source_id=source_id,
            timestamp=timestamp,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            datum_type=datum_type,
            datum_detail=datum_detail,
            value=value,
            unit=unit,
            properties=properties,
        )
        resp = self.client.post(self.record_slug, params=params)
        resp.raise_for_status()
        return RedcordResponse(**resp.json()).assets
