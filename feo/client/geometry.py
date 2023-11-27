from typing import List, Optional, Union

from feo.client import api
from feo.client.api import schemas


class Geometry(schemas.Geometry):
    def __init__(self):
        pass

    @classmethod
    def search(
        cls,
        collection_id: str,
        feature_ids: Optional[Union[str, List[str]]] = None,
        geometry: Optional[schemas.Geometry] = None,
        simplify: Optional[Union[float, str]] = None,
        clip: Optional[bool] = None,
        properties: Optional[dict] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ):
        api.geometries.get()
