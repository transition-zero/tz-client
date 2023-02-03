# template
A template repository for transitionzero to facilitate a common namespace.

## How to use this template
- Customise this README (i.e. delete this section and replace the sections below).
- Delete any directories that you don't need.
- Rename the directory inside transitionzero/ to your module name.
- Don't put an __init__.py file inside transitionzero/ or you'll break things.
- Edit setup.cfg lines 7-8 to reflect the name. Also add requirements to line 13 and below. Add an entrypoint if needed.
- Or if you don't need to pip install this repo, comment out those lines and just edit requirements.txt as needed.

## Description

This section should give a high-level description of the repo and its purpose.

## Contents

This section should describe the contents of this repo.

    <this-repo>/
    ├─ bin/                       # scripts to be run infrequently
    ├─ conf/                      # params and configs, e.g. .yaml
    ├─ data/                      # lightweight* data used in this repo
    ├─ docs/                      # documentation and markdown
    ├─ models/                    # serialised models
    ├─ notebooks/                 # notebooks for prototyping and research
    ├─ tests/                     # unittests for CI/CD
    ├─ transitionzero/            # common tree to ensure nice namespace for imports
    │  ├─ <your-package-name>/    # the actual code library built for this repo
    │     ├─ __init__.py          # the main entrypoint for this library
    ├─ .gitignore                 # standard python gitignore
    ├─ pyproject.toml             # pip install boilerplate
    ├─ setup.py                   # pip install boierplate
    ├─ setup.cfg                  # pip install intructions

*note: heavy data (e.g. > 5mb) should be downloaded from a remote source as part of **Installation** below*

## Installation

This section should contain instructions on how to install the contents of this repo for use, and how to download and configure any large datasets.

    pip install .

## Useage

This section should contain instructions on how to use the contents of this repo. E.g. Entrypoints, configuration, scripts, integrations, etc.

## Development

This section should contain instructions on how to install the repo for development.

    pip install -e .[dev]
    pre-commit install
    pre-commit autoupdate

Run tests:

    tox
