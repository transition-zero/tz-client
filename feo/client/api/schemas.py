from typing import ForwardRef, Optional, Union

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore[no-redef]


class Alias(pydantic.BaseModel):
    node_id: str
    alias: str
    node: Union[ForwardRef("Node"), None]


class Node(pydantic.BaseModel):
    id: str
    node_type: str
    type_alias: str
    name_primary_en: Optional[str] = None
    is_asset: Optional[bool] = None
    properties: Optional[dict] = None
