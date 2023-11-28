"""
    `feo` stands for the Future Energy Outlook, by TransitionZero.
    The Future Energy Outlook gives users the ability to explore historic energy
    data, and to ask research questions about the energy future,
    using TransitionZero's 'batteries-included' systems modelling platform.
    This package, `feo-client`, allows users to interact with the platform via
    both a low-level api wrapper, and a set of higher-order class objects.

    To import the feo client library:
    ```python
    from feo import client
    ```

    Authenticate via the command line with
    ```
    feo auth login
    ```

    To use the lower-level api wrapper:
    ```python
    from feo.client import api
    ```

    To use the high-level objects:
    ```python
    from feo.client import Node, Model, Scenario
    ```
"""

from feo.client.asset import Asset, AssetCollection
from feo.client.geospatial import Features, Geometry
from feo.client.model import Model
from feo.client.node import Node
from feo.client.publisher import Publisher
from feo.client.record import Record, RecordCollection
from feo.client.run import Run
from feo.client.scenario import Scenario
from feo.client.source import Source
from feo.client.technology import Technology

Publisher.model_rebuild()
Source.model_rebuild()

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
