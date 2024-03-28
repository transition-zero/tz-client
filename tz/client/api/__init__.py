"""
    The TransitionZero platform client package, `tz-client`, allows users to interact with the
    platform via both a low-level api wrapper,
    and a set of higher-order class objects.

    First authenticate via the command line
    ```
    tz auth login
    ```

    To import the tz api:
    ```python
    from tz.client import api
    ```

    Calls to underlying data tables can then be made using the api:
    ```python
    nodes = api.nodes.get(id="IDN")
    ```
    ```python
    my_model = api.models.get("my-model")
    ```
"""
from tz.client.api.assets import AssetAPI
from tz.client.api.geospatial import VectorAPI
from tz.client.api.models import ModelAPI
from tz.client.api.node_aliases import NodeAliasAPI
from tz.client.api.nodes import NodeAPI
from tz.client.api.publishers import PublisherAPI
from tz.client.api.records import RecordsAPI
from tz.client.api.runs import RunAPI
from tz.client.api.scenarios import ScenarioAPI
from tz.client.api.sources import SourceAPI
from tz.client.api.technologies import TechnologyAPI

node_aliases = NodeAliasAPI()
nodes = NodeAPI()
assets = AssetAPI()
vectors = VectorAPI()
records = RecordsAPI()
runs = RunAPI()
models = ModelAPI()
scenarios = ScenarioAPI()
sources = SourceAPI()
publishers = PublisherAPI()
technologies = TechnologyAPI()
