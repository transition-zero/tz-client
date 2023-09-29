from __future__ import annotations

import datetime
from typing import Literal

import pandas as pd
from typing_extensions import Self

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore[no-redef]

from feo.client.api.records_api import RecordsApi, _RecordBase


class RecordSearchParams(pydantic.BaseModel):
    node_id: str | None = None
    node_type: str | None = None
    datum_type: str | None = None
    datum_detail: str | None = None
    valid_timestamp_start: datetime.datetime | datetime.date | str | None = None
    valid_timestamp_end: datetime.datetime | datetime.date | str | None = None
    page: int | None = None

    @pydantic.validator("valid_timestamp_start", "valid_timestamp_end", pre=True)
    def parse_timestamp(cls, v):
        # TODO: Check what type of timestamp is expected? datetime, date, str?
        if isinstance(v, (datetime.datetime, datetime.date)):
            return v.isoformat()
        return v


class Record(_RecordBase):
    # Generated fields
    timestamp: str = pydantic.Field(default_factory=datetime.datetime.now().isoformat)

    # Internal fields
    _api: RecordsApi = RecordsApi()

    @classmethod
    def from_dict(self, obj: dict) -> Record:
        """Create an instance of Record from a dict"""
        if obj is None:
            return None
        return Record(**obj)

    def save(self) -> Self:
        # Use create or update
        raise NotImplementedError()

    @classmethod
    def _search(
        cls,
        *,
        node_id: str | None = None,
        node_type: str | None = None,
        datum_type: str | None = None,
        datum_detail: str | None = None,
        valid_timestamp_start: datetime.datetime | datetime.date | str | None = None,
        valid_timestamp_end: datetime.datetime | datetime.date | str | None = None,
        page: int | None = None,
        **kwargs,
    ) -> RecordCollection:
        search_params = RecordSearchParams(
            node_id=node_id,
            node_type=node_type,
            datum_type=datum_type,
            datum_detail=datum_detail,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            page=page,
        )
        res = cls._api.get_v1(**search_params.dict(), **kwargs)
        return RecordCollection(
            records=res["records"],
            next_page=res["next_page"],
            search_params=search_params,
        )

    @classmethod
    def search(
        cls,
        *,
        node_id: str | None = None,
        node_type: str | None = None,
        datum_type: str | None = None,
        datum_detail: str | None = None,
        valid_timestamp_start: datetime.datetime | datetime.date | str | None = None,
        valid_timestamp_end: datetime.datetime | datetime.date | str | None = None,
        page: int | None = None,
        **kwargs,
    ) -> RecordCollection:
        return cls._search(
            node_id=node_id,
            node_type=node_type,
            datum_type=datum_type,
            datum_detail=datum_detail,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            page=page,
            **kwargs,
        )


class RecordCollection(pydantic.BaseModel):
    records: list[Record]
    next_page: int | None = None
    search_params: RecordSearchParams | None = None
    _api: RecordsApi = RecordsApi()

    def __len__(self):
        return len(self.records)

    def __getitem__(self, i):
        return self.records[i]

    def to_dataframe(self) -> pd.DataFrame:
        recs_ = [rec.dict() for rec in self.records]
        df = pd.DataFrame(recs_)
        for col in ["timestamp", "valid_timestamp_start", "valid_timestamp_end"]:
            df[col] = pd.to_datetime(df[col])
        return df

    def next(self, **kwargs) -> RecordCollection:
        """Returns new Record Collection with the next page of results"""
        if self.next_page is None:
            raise ValueError("No next page available")
        next_search_params = self.search_params.copy()
        next_search_params.page = self.next_page
        return Record.search(**next_search_params.dict(), **kwargs)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> RecordCollection:
        """Returns new Record Collection with records from DataFrame"""
        df_ = df.copy()
        for col in ["timestamp", "valid_timestamp_start", "valid_timestamp_end"]:
            df_[col] = df_[col].dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        records = []
        for r in df_.iterrows():
            records.append(dict(r[1]))
        return cls(records=records)

    def save(self) -> RecordCollection:
        """Create or update Record Collection records on the platform."""
        raise NotImplementedError()


class TechnologyParameter(Record):
    datum_type: Literal["technology_parameter"] = "technology_parameter"

    @classmethod
    def search(
        cls,
        *,
        node_id: str | None = None,
        node_type: str | None = None,
        datum_detail: str | None = None,
        valid_timestamp_start: datetime.datetime | datetime.date | str | None = None,
        valid_timestamp_end: datetime.datetime | datetime.date | str | None = None,
        page: int | None = None,
        **kwargs,
    ) -> RecordCollection:
        datum_type = cls.__fields__["datum_type"].default
        return cls._search(
            node_id=node_id,
            node_type=node_type,
            datum_type=datum_type,
            datum_detail=datum_detail,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            page=page,
            **kwargs,
        )


class Generation(Record):
    datum_type: Literal["generation"] = "generation"

    @classmethod
    def search(
        cls,
        *,
        node_id: str | None = None,
        datum_detail: str | None = None,
        valid_timestamp_start: datetime.datetime | datetime.date | str | None = None,
        valid_timestamp_end: datetime.datetime | datetime.date | str | None = None,
        page: int | None = None,
        **kwargs,
    ) -> RecordCollection:
        datum_type = cls.__fields__["datum_type"].default
        return cls._search(
            node_id=node_id,
            datum_type=datum_type,
            datum_detail=datum_detail,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            page=page,
            **kwargs,
        )


class Price(Record):
    datum_type: Literal["price"] = "price"

    @classmethod
    def search(
        cls,
        *,
        node_id: str | None = None,
        node_type: str | None = None,
        datum_detail: str | None = None,
        valid_timestamp_start: datetime.datetime | datetime.date | str | None = None,
        valid_timestamp_end: datetime.datetime | datetime.date | str | None = None,
        page: int | None = None,
        **kwargs,
    ) -> RecordCollection:
        datum_type = cls.__fields__["datum_type"].default
        return cls._search(
            node_id=node_id,
            node_type=node_type,
            datum_type=datum_type,
            datum_detail=datum_detail,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            page=page,
            **kwargs,
        )


class Event(Record):
    datum_type: Literal["event"] = "event"

    @classmethod
    def search(
        cls,
        *,
        node_id: str | None = None,
        node_type: str | None = None,
        datum_detail: str | None = None,
        valid_timestamp_start: datetime.datetime | datetime.date | str | None = None,
        valid_timestamp_end: datetime.datetime | datetime.date | str | None = None,
        page: int | None = None,
        **kwargs,
    ) -> RecordCollection:
        datum_type = cls.__fields__["datum_type"].default
        return cls._search(
            node_id=node_id,
            node_type=node_type,
            datum_type=datum_type,
            datum_detail=datum_detail,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            page=page,
            **kwargs,
        )


class LandCover(Record):
    datum_type: Literal["land_cover"] = "land_cover"

    @classmethod
    def search(
        cls,
        *,
        node_id: str | None = None,
        node_type: str | None = None,
        datum_detail: str | None = None,
        valid_timestamp_start: datetime.datetime | datetime.date | str | None = None,
        valid_timestamp_end: datetime.datetime | datetime.date | str | None = None,
        page: int | None = None,
        **kwargs,
    ) -> RecordCollection:
        datum_type = cls.__fields__["datum_type"].default
        return cls._search(
            node_id=node_id,
            node_type=node_type,
            datum_type=datum_type,
            datum_detail=datum_detail,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            page=page,
            **kwargs,
        )
