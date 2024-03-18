"""
    The TransitionZero platform gives users the ability to explore historic energy
    data, and to ask research questions about the energy future,
    using TransitionZero's 'batteries-included' systems modelling platform.
    This package, `tz-client`, allows users to interact with the platform via
    both a low-level api wrapper, and a set of higher-order class objects.

    To import the tz client library:
    ```python
    from tz import client
    ```

    Authenticate via the command line with
    ```
    tz auth login
    ```

    To use the lower-level api wrapper:
    ```python
    from tz.client import api
    ```

    To use the high-level objects:
    ```python
    from tz.client import Node, Model, Scenario
    ```
"""


from importlib.metadata import PackageNotFoundError, version

from dotenv import load_dotenv

from tz.client.asset import Asset, AssetCollection
from tz.client.geospatial import Features, Geometry
from tz.client.model import Model
from tz.client.node import Node
from tz.client.publisher import Publisher
from tz.client.record import Record, RecordCollection
from tz.client.run import Run
from tz.client.scenario import Scenario
from tz.client.source import Source
from tz.client.technology import Technology

load_dotenv()

Publisher.model_rebuild()
Source.model_rebuild()
Asset.model_rebuild()
Node.model_rebuild()

try:
    __version__ = version("tz-client")
except PackageNotFoundError:
    pass

__all__ = [
    "Node",
    "Asset",
    "AssetCollection",
    "Model",
    "Scenario",
    "Run",
    "Record",
    "RecordCollection",
    "Publisher",
    "Source",
    "Technology",
    "Features",
    "Geometry",
]
