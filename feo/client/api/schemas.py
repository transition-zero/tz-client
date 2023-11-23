from datetime import date, datetime
from typing import Any, ForwardRef, List, Optional, Union

from pydantic import BaseModel, Field


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

    def unpack(self):
        return {
            k: v
            for k, v in {**self.model_dump(), **self.asset_properties.model_dump()}.items()
            if k != "asset_properties"
        }


class Node(NodeBase):
    parents: list[Union[str, "Node"]] | None = None
    children: list[Union[str, "Node"]] | None = None


asset_sector_lookup = {"power": PowerUnit}


class AliasResponse(BaseModel):
    aliases: List[Alias]
    next_page: Optional[int]


class AssetCollectionScope(BaseModel):
    parent_node_id: Optional[str] = None
    sector: Optional[str] = None
    includes: Optional[str] = None


class AssetResponse(BaseModel):
    assets: List[Node]
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


class Record(BaseModel):
    node_id: str | None = Field(None, title="Node Id")
    public: bool | None = Field(None, title="Public")
    source_id: int = Field(..., title="Source Id")
    source_node_id: str | None = Field(None, title="Source Node Id")
    target_node_id: str | None = Field(None, title="Target Node Id")
    timestamp: datetime = Field(..., title="Timestamp")
    valid_timestamp_start: datetime = Field(..., title="Valid Timestamp Start")
    valid_timestamp_end: datetime = Field(..., title="Valid Timestamp End")
    datum_type: str = Field(..., title="Datum Type")
    datum_detail: str = Field(..., title="Datum Detail")
    value: float | None = Field(..., title="Value")
    unit: str = Field(..., title="Unit")
    properties: dict[str, Any] | None = Field(None, title="Properties")
    id: int = Field(..., title="Id")


class RecordResponse(BaseModel):
    records: list[Record] = Field(..., title="Records")
    next_page: int | None = Field(..., title="Next Page")
