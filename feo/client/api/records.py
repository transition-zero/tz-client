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

    def post_csv(self, csv_path: str, publisher_slug: str, source_slug: str) -> int:
        """
        Uploads a CSV file to the server and returns the response as JSON.

        Args:
            csv_path (str): The path to the CSV file.
            publisher_slug (str): The slug of the publisher.
            source_slug (str): The slug of the data source.

        Returns:
            dict: The JSON response from the server.

        Raises:
            requests.HTTPError: If the server returns an error status code.

        Raises a TypeError if any of the arguments are not of type str.
        """
        if not isinstance(csv_path, str):
            raise TypeError("csv_path must be a string")
        if not isinstance(publisher_slug, str):
            raise TypeError("publisher_slug must be a string")
        if not isinstance(source_slug, str):
            raise TypeError("source_slug must be a string")

        provenance_slug = f"{publisher_slug}:{source_slug}"
        with open(csv_path, "rb") as f:
            files = {"file": (csv_path, f)}

            resp = self.client.post(
                f"/records/{provenance_slug}/data",
                files=files,
            )
        resp.raise_for_status()

        return resp.json()
