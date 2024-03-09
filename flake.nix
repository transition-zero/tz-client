{
  inputs.pyproject-nix = {
    url = "github:nix-community/pyproject.nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    { nixpkgs
    , pyproject-nix
    , flake-utils
    , ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        inherit (nixpkgs) lib;
        project = pyproject-nix.lib.project.loadPyproject {
          projectRoot = ./.;
        };
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3.override {
          packageOverrides = self: super: {
            # Note: `pre-commit` is not a package under pythonPackages in
            # nixpkgs; it is a top-level package. So we simply drop it here as
            # a python dependency (it's not used in python _code_ ever), and
            # require it in the devShell as a simple package.
            pre-commit = builtins.null;
          };
        };
      in
      rec
      {
        formatter = pkgs.nixpkgs-fmt;
        devShells.default =
          let
            arg =
              project.renderers.withPackages
                {
                  inherit python;
                  # Install all dependencies; it's probably what we want.
                  extras = [ "geo" "dev" ];
                };
            pythonEnv = python.withPackages arg;
          in
          pkgs.mkShell {
            packages = [
              pythonEnv
              pkgs.pre-commit
            ];

            # We set the Python-path explicitly to this directory so that
            # `pytest` works the same as `python -m pytest` (i.e. it can find
            # the "tests" module.)
            shellHook = "
              export PYTHONPATH=${builtins.toString ./.}
            ";
          };

        packages.default =
          let
            attrs = project.renderers.buildPythonPackage
              {
                inherit python;
                extras = [ "geo" ];
              };
          in
          python.pkgs.buildPythonPackage (attrs // {
            # Note: The version is computed dynamically; but this is not
            # possible in Nix; it would require the version to be in a file in
            # source control.
            #
            # However, we are not using this binary as a distribution, more
            # just as a way to obtain a local binary for development; so we
            # just hard-code the version.
            version = "0.0.0";
          });
      }
    );
}
