from datetime import date
from typing import ForwardRef, List, Optional, Union

from pydantic import BaseModel


class Alias(BaseModel):
    node_id: str
    alias: str
    node: Union[ForwardRef("Node"), None]


class AliasResponse(BaseModel):
    aliases: List[Alias]
    next_page: Optional[int]


class Asset(BaseModel):
    id: str
    node_type: str
    type_alias: str
    unit_type: str
    sector: str
    operating_status: str
    name_primary_en: Optional[str] = None
    public: bool = True
    is_asset: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fuel_type: Optional[str] = None
    capacity: Optional[float] = None
    capacity_unit: Optional[str] = None
    start_date: Optional[date] = None
    retired_date: Optional[date] = None
    technology_detail: Optional[dict] = None
    has_ccs: Optional[bool] = None
    is_captive: Optional[bool] = None
    captive_detail: Optional[dict] = None
    properties: Optional[dict] = None
    other_ids_names: Optional[dict] = None
    ownership_details: Optional[dict] = None


class Node(BaseModel):
    id: str
    node_type: str
    type_alias: str
    name_primary_en: Optional[str] = None
    is_asset: Optional[bool] = None
    properties: Optional[dict] = None
