from datetime import date
from typing import ForwardRef, List, Optional, Union

from pydantic import BaseModel


class Alias(BaseModel):
    node_id: str
    alias: str
    node: Union[ForwardRef("Node"), None]


class PowerUnit(BaseModel):
    # Union of all the params of the asset models
    unit_type: str
    operating_status: str
    latitude: float | None
    longitude: float | None
    fuel_type: str | None
    capacity: float | None
    capacity_unit: str | None
    start_date: date | None
    retired_date: date | None = None
    technology_detail: dict | None
    has_ccs: bool | None
    is_captive: bool | None
    captive_detail: dict | None = None
    properties: dict | None
    other_ids_names: dict | None
    ownership_details: dict | None


class NodeBase(BaseModel):
    id: str
    node_type: str
    type_alias: str
    name_primary_en: str | None = None
    public: bool = True
    is_asset: bool | None = None
    properties: dict | None = None
    sector: str | None = None
    asset_properties: Optional[PowerUnit] = None


class Node(NodeBase):
    parents: list[Union[str, "Node"]] | None = None
    children: list[Union[str, "Node"]] | None = None


class AliasResponse(BaseModel):
    aliases: List[Alias]
    next_page: Optional[int]


class NodeResponse(BaseModel):
    nodes: list[Node]
    representative_node_ids: list[str] | None = None
    node_type_summary: list[dict] | None = None
    gross_capacity: dict[
        str, dict[str, dict[str, float]]
    ] | None = None  # sector, operating_status, unit_type, float
    retiring_capacity: dict[
        str, dict[int, dict[str, float]]
    ] | None = None  # sector, year, unit_type, float
    residual_capacity: dict[
        str, dict[int, dict[str, float]]
    ] | None = None  # sector, year, unit_type, float
