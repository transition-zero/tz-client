from typing import Union

import httpx

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore[no-redef]

from feo.client.api.base import Base


class _RecordBase(pydantic.BaseModel):
    node_id: str
    datum_type: str
    datum_detail: str
    source_id: Union[int, None] = None
    source_node_id: Union[int, None] = None
    target_node_id: Union[int, None] = None
    valid_timestamp_start: Union[str, None] = None
    valid_timestamp_end: Union[str, None] = None
    value: Union[float, None] = None
    unit: Union[str, None] = None
    properties: dict = {}
    public: bool = True


class RecordsAPI(Base):
    def get_v1(
        self,
        node_id: Union[str, None] = None,
        node_type: Union[str, None] = None,
        datum_type: Union[str, None] = None,
        datum_detail: Union[str, None] = None,
        valid_timestamp_start: Union[str, None] = None,
        valid_timestamp_end: Union[str, None] = None,
        page: Union[int, None] = None,
        **kwargs
    ) -> httpx.Response:
        params = {}
        if node_id is not None:
            params["node_id"] = node_id
        if node_type is not None:
            params["node_type"] = node_type
        if valid_timestamp_start is not None:
            params["valid_timestamp_start"] = valid_timestamp_start
        if valid_timestamp_end is not None:
            params["valid_timestamp_end"] = valid_timestamp_end
        if datum_type is not None:
            params["datum_type"] = datum_type
        if datum_detail is not None:
            params["datum_detail"] = datum_detail
        if page is not None:
            params["page"] = page
        res = self.api.get("/records", params=params, **kwargs)
        res.raise_for_status()
        return res.json()

    def post_v1(self, record: _RecordBase) -> httpx.Response:
        raise NotImplementedError()
        # res = self.api.post(
        #     "/records",
        #     json=record.to_dict(),
        # )
        # res.raise_for_status()
        # return res.json()
