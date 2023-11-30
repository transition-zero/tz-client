"""
    `feo` stands for Future Energy Outlook, by TransitionZero.
    The Future Energy Outlook package, `feo-client`, allows users to interact with the
    platform via both a low-level api wrapper,
    and a set of higher-order class objects.

    First authenticate via the command line
    ```
    feo auth login
    ```

    To import the feo api:
    ```python
    from feo.client import api
    ```

    Calls to underlying data tables can then be made using the api:
    ```python
    nodes = api.nodes.get(id="IDN")
    ```
    ```python
    my_model = api.models.get("my-model")
    ```
"""
from feo.client.api.aliases import AliasAPI
from feo.client.api.assets import AssetAPI
from feo.client.api.geospatial import VectorAPI
from feo.client.api.models import ModelAPI
from feo.client.api.nodes import NodeAPI
from feo.client.api.publishers import PublisherAPI
from feo.client.api.records import RecordsAPI
from feo.client.api.runs import RunAPI
from feo.client.api.scenarios import ScenarioAPI
from feo.client.api.sources import SourceAPI
from feo.client.api.technologies import TechnologyAPI

aliases = AliasAPI()
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
