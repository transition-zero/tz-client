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


class Node(NodeBase):
    parents: list[Union[str, "Node"]] | None = None
    children: list[Union[str, "Node"]] | None = None


class AliasResponse(BaseModel):
    aliases: List[Alias]
    next_page: Optional[int]


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


class ModelScenarioRunLink(BaseModel):
    url: str = Field(..., title="Url")
    title: str = Field(..., title="Title")
    properties: dict[str, Any] | None = Field(..., title="Properties")
    type: str = Field(..., title="Type")


class RunBase(BaseModel):
    name: str = Field(..., title="Name")
    slug: str | None = Field(None, title="Slug")
    description: str = Field(..., title="Description")
    public: bool = Field(..., title="Public")
    scenario_slug: str = Field(..., title="Scenario Slug")
    model_slug: str = Field(..., title="Model Slug")
    data: dict[str, Any] | None = Field(None, title="Data")
    featured: bool | None = Field(None, title="Featured")
    status: str = Field(..., title="Status")
    links: list[ModelScenarioRunLink] | None = Field(None, title="Links")
    capacity_datetime_convention: str | None = Field(None, title="Capacity Datetime Convention")
    production_datetime_convention: str | None = Field(None, title="Production Datetime Convention")
    flow_datetime_convention: str | None = Field(None, title="Flow Datetime Convention")
    preview_image_url: str | None = Field(None, title="Preview Image Url")


class TimeScopeContiguous(BaseModel):
    resolution_hourly: int = Field(..., title="Resolution Hourly")


class TimeScopeSlicePart(BaseModel):
    id: str = Field(..., title="Id")
    description: str = Field(..., title="Description")


class TimeScopeSlices(BaseModel):
    parts: list[TimeScopeSlicePart] | None = Field(None, title="Parts")
    dayparts: list[TimeScopeSlicePart] | None = Field(None, title="Dayparts")
    yearparts: list[TimeScopeSlicePart] | None = Field(None, title="Yearparts")


class TimeScopeOutput(BaseModel):
    contiguous: TimeScopeContiguous | None = None
    representative_slices: TimeScopeSlices | None = None


class UserNameplate(BaseModel):
    id: str = Field(..., title="Id")
    email: str = Field(..., title="Email")
    username: str = Field(..., title="Username")


class NodeSummary(BaseModel):
    capacity_summary: float | None = Field(None, title="Capacity Summary")


class NodeTypeSummaryElement(BaseModel):
    type_alias: str = Field(..., title="Type Alias")
    node_count: int = Field(..., title="Node Count")


class ScenarioBase(BaseModel):
    name: str = Field(..., title="Name")
    version: str = Field(..., title="Version")
    slug: str | None = Field(None, title="Slug")
    model_slug: str = Field(..., title="Model Slug")
    public: bool = Field(..., title="Public")
    description: str | None = Field(..., title="Description")
    featured: bool | None = Field(None, title="Featured")
    status: str = Field(..., title="Status")
    links: list[ModelScenarioRunLink] | None = Field(None, title="Links")
    data: dict[str, Any] | None = Field(None, title="Data")


class Scenario(ScenarioBase):
    owner_id: str = Field(..., title="Owner Id")
    model: "Model | None" = None
    owner: UserNameplate | None = None
    runs: "list[Run] | None" = Field(None, title="Runs")
    featured_run: "Run| None" = None
    preview_image_url: str | None = Field(None, title="Preview Image Url")


class Model(BaseModel):
    name: str | None = Field(None, title="Name")
    slug: str = Field(..., title="Slug")
    description: str | None = Field(None, title="Description")
    version: str = Field(..., title="Version")
    time_scope: TimeScopeOutput
    datetime_range_start: datetime = Field(..., title="Datetime Range Start")
    datetime_range_end: datetime = Field(..., title="Datetime Range End")
    sectors: list[str] = Field(..., title="Sectors")
    status: str | None = Field(None, title="Status")
    node_ids: list[str] = Field(..., title="Node Ids")
    representative_node_ids: list[str] = Field(..., title="Representative Node Ids")
    public: bool = Field(..., title="Public")
    featured: int | None = Field(None, title="Featured")
    data: dict[str, Any] | None = Field(None, title="Data")
    links: list[ModelScenarioRunLink] | None = Field(None, title="Links")
    owner_id: str = Field(..., title="Owner Id")
    views: int | None = Field(None, title="Views")
    stars: int | None = Field(None, title="Stars")
    owner: UserNameplate | None = None
    scenarios: list[Scenario] | None = Field(None, title="Scenarios")
    node_type_summary: list[NodeTypeSummaryElement] = Field(..., title="Node Type Summary")
    featured_scenario: Scenario | None = None
    preview_image_url: str | None = Field(None, title="Preview Image Url")


class RunSingleExtrema(BaseModel):
    max_value: float | None = Field(..., title="Max Value")
    min_value: float | None = Field(..., title="Min Value")
    max_datetime: datetime | None = Field(..., title="Max Datetime")
    min_datetime: datetime | None = Field(..., title="Min Datetime")


class RunExtrema(BaseModel):
    capacity_node_gross: RunSingleExtrema | None = None
    capacity_node_new: RunSingleExtrema | None = None
    capacity_node_retirements: RunSingleExtrema | None = None
    capacity_node_residual: RunSingleExtrema | None = None
    capacity_edge_gross: RunSingleExtrema | None = None
    capacity_edge_new: RunSingleExtrema | None = None
    capacity_edge_retirements: RunSingleExtrema | None = None
    capacity_edge_residual: RunSingleExtrema | None = None
    flow: RunSingleExtrema | None = None
    production: RunSingleExtrema | None = None
    global_start_datetime: datetime | None = Field(..., title="Global Start Datetime")
    global_end_datetime: datetime | None = Field(..., title="Global End Datetime")


class Metric(BaseModel):
    metric: str = Field(..., title="Metric")
    unit: str = Field(..., title="Unit")
    value: float = Field(..., title="Value")


class Run(RunBase):
    owner_id: str = Field(..., title="Owner Id")
    model: Model | None = None
    scenario: Scenario | None = None
    owner: UserNameplate | None = None
    nodes: list[str] | None = Field(None, title="Nodes")
    valid_datetimes: list[str] | None = Field(None, title="Valid Datetimes")
    extrema: RunExtrema | None = None
    capacity: dict[str, Any] | None = Field(None, title="Capacity")
    production: dict[str, Any] | None = Field(None, title="Production")
    flow: dict[str, Any] | None = Field(None, title="Flow")
    marginal_cost: dict[str, Any] | None = Field(None, title="Marginal Cost")
    system_cost: dict[str, Any] | None = Field(None, title="System Cost")
    profiles: dict[str, Any] | None = Field(None, title="Profiles")
    metrics: list[Metric] | None = Field(None, title="Metrics")


class RunQueryResult(BaseModel):
    runs: list[Run] = Field(..., title="Runs")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")


class ScenarioQueryResult(BaseModel):
    scenarios: list[Scenario] = Field(..., title="Scenarios")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")
