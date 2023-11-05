<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/transition-zero/.github/raw/main/profile/img/logo-dark.png">
  <img alt="TransitionZero Logo" width="1000px" src="https://github.com/transition-zero/.github/raw/main/profile/img/logo-light.png">
  <a href="https://www.transitionzero.org/">
</picture>

# Future Energy Outlook Python Client

<img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Lkruitwagen/feffb38d46c750cad5402dca5dd54bf9/raw/713dc1d51bcfb95d520aa72a19e5029b387b8e3c/tests_passing.json" alt="Tests Passing"><img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Lkruitwagen/d2b6ec23e3c6e8309236216689d91782/raw/456f94a2a084bfffa07db241b4c82bbcc668bdf4/coverage_badge.json" alt="Test Coverage"><img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Lkruitwagen/bd1e357c1bce5fc2c0808bcdb569157c/raw/3fb7a23af07abaf2fbdf55944545bc97f46f1070/python_version_badge.json" alt="Supported Python versions"><img src="https://img.shields.io/badge/under%20construction-ffae00" alt="Supported Python versions">


**Documentation**: <a href="https://docs.feo.transitionzero.org" target="_blank">https://docs.feo.transitionzero.org</a>

**API Reference**: <a href="https://api.feo.transitionzero.org/latest/docs" target="_blank">https://api.feo.transitionzero.org/latest/docs</a>

**Future Energy Outlook**: <a href="https://feo.transitionzero.org" target="_blank">https://feo.transitionzero.org</a>

---

The _Future Energy Outlook_ is TransitionZero's open-access energy transition research platform.
This Python Client gives programmatic access to all the functionality of the FEO platform:

* **Open Data**: Asset-level and historical data free to access, forever.
* **No-barriers Systems Modelling**: Begin asking your energy transition research questions with a simple UI or a few lines of code.
* **Transparent Data Provenance**: Trace all data back to its origin.
* **Reproduceable**: Built with open-source systems modelling frameworks, with transparent or user-defined assumptions.
* **Social and Shareable**: Share systems models reports publicly and star your favourites.
* **Analysis-Ready outputs**: Download analysis-ready spreadsheets.
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

### Accessing asset-level data

### Accessing historical data

### Accessing systems models and reports

### Simple API calls



## Documentation

The full documentation for FEO can be found here: <a href="https://docs.feo.transitionzero.org" target="_blank">https://docs.feo.transitionzero.org</a>

## Contributing

## License
