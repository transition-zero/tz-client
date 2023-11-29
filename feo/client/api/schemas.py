from datetime import date, datetime
from typing import Annotated, Any, Dict, List, Literal, Optional, Tuple, Union
from warnings import warn

from pydantic import BaseModel, ConfigDict, Field, conlist, field_validator
from shapely import from_geojson  # type: ignore

try:
    # Setting mypy to ignore due to missing stubs
    import geopandas as gpd  # type: ignore

    GPD_SUPPORT = True
except ImportError:
    GPD_SUPPORT = False
    warn(
        "Failed to locate 'geo' dependencies. Geospatial functionality will be limited."
        " For full geospatial support please install the 'geo' requirements:"
        " pip install feo-client[geo]"
    )


class PydanticBaseModel(BaseModel):
    # avoid protected 'model_' namespace
    model_config = ConfigDict(protected_namespaces=())


class PowerUnit(PydanticBaseModel):
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


class NodeBase(PydanticBaseModel):
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
            for k, v in {
                **self.model_dump(),
                **self.asset_properties.model_dump(),
            }.items()
            if k != "asset_properties"
        }


class Node(NodeBase):
    parents: list[Union[str, "Node"]] | None = None
    children: list[Union[str, "Node"]] | None = None


asset_sector_lookup = {"power": PowerUnit}


class Alias(PydanticBaseModel):
    node_id: str
    alias: str
    node: Node | None


class AliasResponse(PydanticBaseModel):
    aliases: List[Alias]
    next_page: Optional[int]


class CollectionScope(PydanticBaseModel):
    node_id: Optional[str] = None
    parent_node_id: Optional[str] = None
    sector: Optional[str] = None
    includes: Optional[str] = None


class AssetResponse(PydanticBaseModel):
    assets: List[Node]
    next_page: Optional[int]


class NodeResponse(PydanticBaseModel):
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


class Geometry(PydanticBaseModel):
    type: str
    coordinates: Union[PolygonCoords, MultiPolygonCoords, Point]

    @field_validator("type", mode="before")
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
        return from_geojson(self.to_geojson())


class FeatureBase(PydanticBaseModel):
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


class FeatureCollection(PydanticBaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[Feature]
    next_page: Optional[int] = None

    def to_dict(self):
        return self.model_dump()

    def to_geojson(self):
        return self.model_dump_json()

    def to_geodataframe(self):
        if GPD_SUPPORT:
            return gpd.read_file(self.to_geojson(), driver="GeoJSON")
        else:
            raise NotImplementedError(
                "Full geospatial support not available."
                " Please install 'geo' depencencies to use this method:"
                " pip install feo-client[geo]"
            )


class RecordID(PydanticBaseModel):
    id: int = Field(..., title="Id")


class RecordBase(PydanticBaseModel):
    node_id: str | None = Field(None, title="Node Id")
    public: bool | None = Field(None, title="Public")
    source_id: int = Field(..., title="Source Id")
    source_node_id: str | None = Field(None, title="Source Node Id")
    target_node_id: str | None = Field(None, title="Target Node Id")
    timestamp: datetime = Field(..., title="Timestamp")
    valid_timestamp_start: datetime = Field(..., title="Valid Timestamp Start")
    valid_timestamp_end: datetime = Field(..., title="Valid Timestamp End")
    datum_type: str = Field(..., title="Datum Type")
    datum_detail: str | None = Field(None, title="Datum Detail")
    value: float | None = Field(..., title="Value")
    unit: str = Field(..., title="Unit")
    properties: dict[str, Any] | None = Field(None, title="Properties")


class Record(RecordID, RecordBase):
    pass


class RecordsResponse(PydanticBaseModel):
    records: list[Record] = Field(..., title="Records")
    next_page: int | None = Field(..., title="Next Page")


class ModelScenarioRunLink(PydanticBaseModel):
    url: str = Field(..., title="Url")
    title: str = Field(..., title="Title")
    properties: dict[str, Any] | None = Field(..., title="Properties")
    type: str = Field(..., title="Type")


class TimeScopeContiguous(PydanticBaseModel):
    resolution_hourly: int = Field(..., title="Resolution Hourly")


class TimeScopeSlicePart(PydanticBaseModel):
    id: str = Field(..., title="Id")
    description: str = Field(..., title="Description")


class TimeScopeSlices(PydanticBaseModel):
    parts: list[TimeScopeSlicePart] | None = Field(None, title="Parts")
    dayparts: list[TimeScopeSlicePart] | None = Field(None, title="Dayparts")
    yearparts: list[TimeScopeSlicePart] | None = Field(None, title="Yearparts")


class TimeScopeOutput(PydanticBaseModel):
    contiguous: TimeScopeContiguous | None = None
    representative_slices: TimeScopeSlices | None = None


class UserNameplate(PydanticBaseModel):
    id: str = Field(..., title="Id")
    email: str = Field(..., title="Email")
    username: str = Field(..., title="Username")


class NodeSummary(PydanticBaseModel):
    capacity_summary: float | None = Field(None, title="Capacity Summary")


class NodeTypeSummaryElement(PydanticBaseModel):
    type_alias: str = Field(..., title="Type Alias")
    node_count: int = Field(..., title="Node Count")


class ScenarioBase(PydanticBaseModel):
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
    owner_id: str = Field(..., title="Owner Id")
    owner: UserNameplate | None = None
    preview_image_url: str | None = Field(None, title="Preview Image Url")


class Scenario(ScenarioBase):
    model: "Model | None" = None
    runs: "list[Run] | None" = Field(None, title="Runs")
    featured_run: "Run| None" = None


class ModelBase(PydanticBaseModel):
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
    node_type_summary: list[NodeTypeSummaryElement] = Field(..., title="Node Type Summary")
    preview_image_url: str | None = Field(None, title="Preview Image Url")


class Model(ModelBase):
    scenarios: list[Scenario] | None = Field(None, title="Scenarios")
    featured_scenario: Scenario | None = None


class RunSingleExtrema(PydanticBaseModel):
    max_value: float | None = Field(..., title="Max Value")
    min_value: float | None = Field(..., title="Min Value")
    max_datetime: datetime | None = Field(..., title="Max Datetime")
    min_datetime: datetime | None = Field(..., title="Min Datetime")


class RunExtrema(PydanticBaseModel):
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


class Metric(PydanticBaseModel):
    metric: str = Field(..., title="Metric")
    unit: str = Field(..., title="Unit")
    value: float = Field(..., title="Value")


class RunBase(PydanticBaseModel):
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
    owner_id: str = Field(..., title="Owner Id")
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


class Run(RunBase):
    model: Model | None = None
    scenario: Scenario | None = None


class RunQueryResult(PydanticBaseModel):
    runs: list[Run] = Field(..., title="Runs")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")


class ModelQueryResult(PydanticBaseModel):
    models: list[Model] = Field(..., title="Models")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")


class ScenarioQueryResult(PydanticBaseModel):
    scenarios: list[Scenario] = Field(..., title="Scenarios")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")


class Publisher(PydanticBaseModel):
    name: str
    short_name: str
    url: str | None = None
    public: bool = True
    organisation_type: str
    slug: str


class PublisherQueryResponse(PydanticBaseModel):
    publishers: list[Publisher]
    next_page: int | None


class License(PydanticBaseModel):
    abbreviation: str
    name: str
    full_text: str
    public: bool = True


class Link(PydanticBaseModel):
    url: str
    url_type: str
    source_id: int
    public: bool = True


class Source(PydanticBaseModel):
    name: str
    short_name: str
    public: bool
    year: int | None = None
    month: int | None = None
    day: int | None = None
    quarter: int | None = None
    description: str
    license_abbrv: str | None = None
    publisher_slug: str | None = None
    slug: str | None = None
    base_license: License | None = Field(None, alias="license")
    base_links: List[Link] | None = Field(None, alias="links")


class SourceQueryResponse(PydanticBaseModel):
    next_page: int | None
    sources: list[Source]


class TechnologyBase(PydanticBaseModel):
    uuid: str = Field(..., title="UUID")
    slug: str = Field(..., title="Slug")
    name: str | None = Field(None, title="Name")
    owner_id: str = Field(..., title="Owner Id")
    public: bool = Field(..., title="Public")
    properties: dict | None = Field(None, title="Technology Parameters")
    parents: list | None = Field(None, title="Parent Technologies")
    children: list | None = Field(None, title="Child Technologies")


class Technology(TechnologyBase):
    parents: list[Union[str, "Technology"]] | None = Field(None, title="Parent Technologies")
    children: list[Union[str, "Technology"]] | None = Field(None, title="Child Technologies")


class TechnologyQueryResponse(PydanticBaseModel):
    technologies: list[Technology] = Field(..., title="Technologies")
    page: int | None = Field(None, title="Page")
    total_pages: int | None = Field(None, title="Total Pages")
