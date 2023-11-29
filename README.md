<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/transition-zero/.github/raw/main/profile/img/logo-dark.png">
  <img alt="TransitionZero Logo" width="1000px" src="https://github.com/transition-zero/.github/raw/main/profile/img/logo-light.png">
  <a href="https://www.transitionzero.org/">
</picture>


# Future Energy Outlook Python Client

<!-- badges-begin -->

[![License][license badge]][license]
[![Contributor Covenant][contributor covenant badge]][code of conduct]
![Tests][tests badge]
![Coverage][coverage badge]
![Python][python badge]
![Status][status badge]

[license badge]: https://img.shields.io/badge/License-Apache_2.0-blue.svg
[license]: https://opensource.org/licenses/Apache-2.0

[contributor covenant badge]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
[code of conduct]: https://github.com/transition-zero/feo-client/blob/main/CODE-OF-CONDUCT.md

[tests badge]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Lkruitwagen/feffb38d46c750cad5402dca5dd54bf9/raw/tests_passing.json

[coverage badge]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Lkruitwagen/d2b6ec23e3c6e8309236216689d91782/raw/coverage_badge.json

[python badge]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Lkruitwagen/bd1e357c1bce5fc2c0808bcdb569157c/raw/python_version_badge.json

[status badge]: https://img.shields.io/badge/under%20construction-ffae00

<!-- badges-end -->

**Documentation**: <a href="https://docs.feo.transitionzero.org" target="_blank">https://docs.feo.transitionzero.org</a>

**API Reference**: <a href="https://api.feo.transitionzero.org/latest/docs" target="_blank">https://api.feo.transitionzero.org/latest/docs</a>

**Future Energy Outlook**: <a href="https://feo.transitionzero.org" target="_blank">https://feo.transitionzero.org</a>

---

The _Future Energy Outlook_ (FEO) is TransitionZero's open-access energy transition research platform.
This Python Client gives programmatic access to all the functionality of the FEO platform:

* **Open Data**: Asset-level and historical data free to access, forever.
* **No-barriers Systems Modelling**: Begin asking your energy transition research questions with a simple UI or a few lines of code.
* **Transparent Data Provenance**: Trace all data back to its origin.
* **Reproduceable**: Built with open-source systems modelling frameworks, with transparent or user-defined assumptions.
* **Social and Shareable**: Share systems models reports publicly and star your favourites.
* **Analysis-Ready Outputs**: Download analysis-ready spreadsheets.
* **Flagship Analysis**: Access premier research outputs prepared by TransitionZero researchers.


---

## Installation

The latest release of the FEO Python Client can be installed via `pip`.

    pip install feo-client

The client can also be installed from this repo, for any features not yet available via the Python Package Index:

    pip install git+https://github.com/transition-zero/feo-client.git@main

## Authentication

To access resources via the Python Client you must have a (free) FEO account. An account can be created [here](https://feo.transitionzero.org).

To log in for programmatic access, use the feo command-line tool:

    feo auth login

You'll be invited to login via a browser, verify a device code and then will be redirected to your terminal.
An access token will be stored in your machine's home directory at `.tz-feo/token.json`.

The feo login can also be called directly (for example via a Jupyter notebook):

    from feo.client.auth import login
    login()

## Quickstart

The FEO client provides object-level interfaces to the main FEO building blocks. Users may also use the underlying API wrapper.

### Accessing node-level data

In the FEO platform, all data is indexed to a `Node`. Nodes are used to represent useful physical and administrative boundaries - ranging from individual physical assets through to entire countries and continents. This flexibility allows FEO users to access data at all levels of aggregation via the FEO platform .

In the physics of systems modelling, Nodes are discrete units around which the continuity of energy and materials is constrained. In other words, at every node in a systems model, the input plus supply to the node must equal the output plus demand.
To begin, import the `Node` client.
```
from feo.client import Node
```

The `Node.search` method can be used to search for Nodes.
```
Node.search("Bali")
```

Each search result is an instance of the `Node` object.
```
IDN = Node.search("indonesia")[0]
IDN
```

Nodes have an `id` which is unique. Nodes can have many names (or `aliases`), one of which is attached to the node as a primary English name.
```
IDN.id, IDN.name_primary_en
```

### Accessing asset-level data

In the FEO platform, `Assets` are a subset of Nodes. Assets are Nodes which correspond to physical plant and equipment like power stations and steelworks.

To begin, import the Asset client.
```
from feo.client import Asset
```

Like nodes, assets can be searched for:
```
search_results = Asset.search("Banten Suralaya power", sector="power")
for asset in search_results:
    print(asset.id, asset.name_primary_en)
```

... or directly instantiated:
```
asset = Asset.from_id("PWRCOAIDNA0U0")
asset.id, asset.name_primary_en
```

### Accessing historical data

### Accessing systems models and reports

System Models are representations of energy and material flows, usually optimised by economic logic like least-costs-minimisation.

System models in FEO are composed of three objects - Models, Scenarios, and Runs.

- **Models** describe the geographic, temporal, and sectoral scope of the systems model.
- **Scenarios** are narrative counter-factuals of the future, which may be accompanied by numeric projections
- **Runs** are solutions to parameterised systems models, used to explore uncertainty

Models, Scenarios, and Runs can be imported from the client:
```
from feo.client import Model, Scenario, Run
```

The `Model` client can be used to search and retrieve model objects.
```
Model.search(model_slug='feo-global-indonesia')
```

Models can also be retrieved directly by id
```
idn_model = Model.from_id('feo-global-indonesia')
```

Scenarios associated can also be retrieved from the model object.
```
idn_model.scenarios
```

... as can the runs associated with scenarios
```
run = idn_model.scenarios[0].runs
```

### Simple API calls



## Documentation

The full documentation for FEO can be found here: <a href="https://docs.feo.transitionzero.org" target="_blank">https://docs.feo.transitionzero.org</a>

## Contributing

## License
