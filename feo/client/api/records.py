import datetime
from typing import List

from feo.client.api.base import BaseAPI
from feo.client.api.schemas import Record, RecordsResponse


class RecordsAPI(BaseAPI):
    def get(
        self,
        node_id: list[str] | str | None = None,
        public: bool = True,
        timestamp: datetime.datetime | str | None = None,
        valid_timestamp_start: datetime.datetime | str | None = None,
        valid_timestamp_end: datetime.datetime | str | None = None,
        provenance_slug: list[str] | str | None = None,
        technology: str | None = None,
        datum_type: list[str] | str | None = None,
        datum_detail: list[str] | str | None = None,
        node_type: list[str] | str | None = None,
        value: float | None = None,
        unit: list[str] | str | None = None,
        properties: dict | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> List[Record]:
        params = dict(
            node_id=node_id,
            public=public,
            timestamp=timestamp,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            provenance_slug=provenance_slug,
            technology=technology,
            datum_type=datum_type,
            datum_detail=datum_detail,
            node_type=node_type,
            value=value,
            unit=unit,
            properties=properties,
            limit=limit,
            page=page,
        )

        resp = self.client.get("/records", params=params)
        resp.raise_for_status()

        return RecordsResponse(**resp.json()).records
