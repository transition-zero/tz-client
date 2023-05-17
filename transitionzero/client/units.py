from datetime import date
from typing import List, Optional, Union

import httpx

from transitionzero.client.base import Base


class Units(Base):
    def __init__(self):
        super().__init__()
        self.client = httpx.Client(
            base_url="https://node-data.feo.transitionzero.org/",
            headers=self.headers,
        )

    def search_units(
        self,
        unit_id: Optional[Union[str, List[str]]] = None,
        asset_id: Optional[Union[str, List[str]]] = None,
        admin_0: Optional[Union[str, List[str]]] = None,
        admin_1: Optional[Union[str, List[str]]] = None,
        unit_type: Optional[Union[str, List[str]]] = None,
        region: Optional[Union[str, List[str]]] = None,
        operating_status: Optional[Union[str, List[str]]] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        fuel_type: Optional[Union[str, List[str]]] = None,
        capacity: Optional[float] = None,
        capacity_upper_bound: Optional[float] = None,
        capacity_lower_bound: Optional[float] = None,
        capacity_unit: Optional[Union[str, List[str]]] = None,
        start_date: Optional[date] = None,
        start_date_upper_bound: Optional[date] = None,
        start_date_lower_bound: Optional[date] = None,
        retired_date: Optional[date] = None,
        technology_detail: Optional[str] = None,
        has_css: Optional[bool] = None,
        is_captive: Optional[bool] = None,
        captive_detail: Optional[str] = None,
        properties: Optional[str] = None,
        other_ids_names: Optional[str] = None,
        ownership_details: Optional[str] = None,
        format: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {
            "unit_id": unit_id,
            "asset_id": asset_id,
            "admin_0": admin_0,
            "admin_1": admin_1,
            "unit_type": unit_type,
            "region": region,
            "operating_status": operating_status,
            "latitude": latitude,
            "longitude": longitude,
            "fuel_type": fuel_type,
            "capacity": capacity,
            "capacity_upper_bound": capacity_upper_bound,
            "capacity_lower_bound": capacity_lower_bound,
            "capacity_unit": capacity_unit,
            "start_date": start_date,
            "start_date_upper_bound": start_date_upper_bound,
            "start_date_lower_bound": start_date_lower_bound,
            "retired_date": retired_date,
            "retired_date": retired_date,
            "technology_detail": technology_detail,
            "has_css": has_css,
            "is_captive": is_captive,
            "captive_detail": captive_detail,
            "properties": properties,
            "other_ids_names": other_ids_names,
            "ownership_details": ownership_details,
            "format": format,
            "limit": limit,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}
        r = self.client.get("latest/units", params=params)

        self.catch_errors(r)

        return r.json()
