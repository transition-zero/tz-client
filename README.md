<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/transition-zero/.github/raw/main/profile/img/logo-dark.png">
  <img alt="TransitionZero Logo" width="1000px" src="https://github.com/transition-zero/.github/raw/main/profile/img/logo-light.png">
  <a href="https://www.transitionzero.org/">
</picture>

# Future Energy Outlook Python Client

< !-- *badges here* --/>


**Documentation**: <a href="https://docs.feo.transitionzero.org" target="_blank">https://docs.feo.transitionzero.org</a>

**API Reference**: <a href="https://api.feo.transitionzero.org/latest/docs", target="_blank">https://api.feo.transitionzero.org/latest/docs</a>

**Future Energy Outlook**: <a href="https://feo.transitionzero.org" target="_blank">https://feo.transitionzero.org</a>

---

The _Future Energy Outlook_ is TransitionZero's open-access energy transition research platform.

The key features are:

* **Open Data**: Asset-level and historical data free to access, forever.
* **No-barriers Systems Modelling**: Begin asking your energy transition research questions with a simple UI or a few lines of code.
* **Transparent and Reproduceable**: Built with open-source systems modelling frameworks, with transparent or user-defined assumptions.
* **Social and Shareable**: Share systems models reports publicly and star your favs.
* **Analysis-Ready outputs**: Download analysis-ready excel workbooks.
* **Flagship Analysis**: Access premier research outputs prepared by TransitionZero researchers.

This Python Client gives programmatic access to all the functionality of the FEO platform.

---

## Installation

The latest release of the FEO Python Client can be installed via `pip`.

    pip install feo-client

The client can also be installed from this repo, for any features not yet available via the Python Package Index:

    pip install git+https

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

The FEO client is provided with two interface levels: a base-level `api` interface and object-level interface.

### Simple API calls



## Documentation

## Contributing

## License
