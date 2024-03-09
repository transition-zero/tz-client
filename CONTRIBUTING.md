All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

If you are simply looking to start working with the codebase, navigate to the GitHub "issues" tab and start looking through interesting issues. There are a number of issues listed under Docs and good first issue where you could start out.

Feel free to ask questions on the mailing list or on Slack.

As contributors and maintainers to this project, you are expected to abide by TransitionZero's code of conduct. More information can be found in the [Code of Conduct](CODE-OF-CONDUCT.md).

## Installing dev dependencies

```console
git clone https://github.com/transition-zero/feo-client.git
cd feo-client
pip install ".[dev]"
```

To install pre-commit hooks (recommended), run

```console
pre-commit install
```

Please also run mypy with

```console
pip install ".[dev]" && mypy -p feo.client
```

## Authentication

Running our test suite first requires authentication

```console
feo auth login
```

## Running tests

```console
pytest
```

After having made changes in the codebase, run `pip install ".[dev]"` to pick them up in the tests.

## Nix

We have provided a [nix](https://nixos.org/)
[flake](https://nixos.wiki/wiki/Flakes) if you wish to use it.

We make use of [pyproject.nix](https://github.com/nix-community/pyproject.nix)
to grab the dependencies from the [pyproject.toml](./pyproject.toml) file, and
we enable all optional dependencies.

There are a couple of quirks:

1. pyproject.nix does make the `project.scripts` binaries available in the
   shell: <https://github.com/nix-community/pyproject.nix/issues/67>
   - To get the binary, you may run `nix build .` and find it at
   `./result/bin/feo`.
2. The dynamic version doesn't play well with Nix for two reasons:
  - Nix needs a static version for building the package, so we just set it to
     `0.0.0`,
  - pyproject.nix does not actually _install_ the package, so importlib is
     unable to find it's version: <https://github.com/nix-community/pyproject.nix/issues/66>

Note that for the pre-commit hooks, one might ideally use
[pre-commit-hooks.nix](https://github.com/cachix/pre-commit-hooks.nix) but
this requires you to define and configure the hooks in the flake.nix file,
which then generates the `.pre-commit-config.yaml` file; i.e. it requires nix
to make changes to the hooks; but we want nix to be optional, so we leave it
as-is for now.

As a result, you should run `pre-commit install` to install the hooks, once in
the dev shell.
