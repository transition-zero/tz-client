from datetime import date, datetime
from typing import Annotated, Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, Field, conlist, validator

try:
    # Setting mypy to ignore due to missing stubs
    from shapely import from_geojson  # type: ignore

    GEO_SUPPORT = True
except ImportError:
    GEO_SUPPORT = False


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


class Alias(BaseModel):
    node_id: str
    alias: str
    node: Node | None


class AliasResponse(BaseModel):
    aliases: List[Alias]
    next_page: Optional[int]


class CollectionScope(BaseModel):
    node_id: Optional[str] = None
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


Point = Tuple[float, float]
LinearRing = Annotated[List[Point], conlist(Point, min_length=4)]
PolygonCoords = Annotated[List[LinearRing], conlist(LinearRing, min_length=1)]
MultiPolygonCoords = Annotated[List[PolygonCoords], conlist(PolygonCoords, min_length=1)]
BBox = Tuple[float, float, float, float]  # 2D bbox
VALID_GEOM_TYPES = [
    "Polygon",
    "Point",
    "LineString",
    "MultiPolygon",
    "MultiPoint",
    "MultiLineString",
]


class Geometry(BaseModel):
    type: str
    coordinates: Union[PolygonCoords, MultiPolygonCoords, Point]

    @validator("type")
    def validate_type(cls, geom_type):
        if geom_type in VALID_GEOM_TYPES:
            return geom_type
        else:
            raise ValueError(f"Must be one of {', '.join(VALID_GEOM_TYPES)}")

    def to_dict(self):
        return self.model_dump()

    def to_geojson(self):
        return self.model_dump_json()

    def to_shape(self):
        if GEO_SUPPORT:
            return from_geojson(self.to_geojson())
        else:
            raise NotImplementedError


class FeatureBase(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: Optional[Dict] = dict()

    def to_geojson(self):
        return {
            "type": self.type,
            "geometry": self.geometry.to_geojson(),
            "properties": self.properties,
            "id": self.id,
        }


class Feature(FeatureBase):
    collection_slug: str
    slug: str


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[Feature]
    next_page: Optional[int] = None

    def to_geodataframe(self):
        if GEO_SUPPORT:
            pass
        else:
            raise NotImplementedError


class RecordID(BaseModel):
    id: int = Field(..., title="Id")


class RecordBase(BaseModel):
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


class Record(RecordID, RecordBase):
    class Config:
        orm_mode: bool = True


class RecordsResponse(BaseModel):
    records: list[Record] = Field(..., title="Records")
    next_page: int | None = Field(..., title="Next Page")


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


class ModelQueryResult(BaseModel):
    models: list[Model] = Field(..., title="Models")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")


class ScenarioQueryResult(BaseModel):
    scenarios: list[Scenario] = Field(..., title="Scenarios")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")
