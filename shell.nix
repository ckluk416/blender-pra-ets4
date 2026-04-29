{ pkgs ? import <nixpkgs> {} }:

let
  my-python-packages = ps: with ps; [
    pandas
    numpy
    requests
    # scipy
    # matplotlib
  ];

  my-python = pkgs.python3.withPackages my-python-packages;

in
pkgs.mkShell {
  name = "blender-dev-shell";

  buildInputs = [
    pkgs.blender
    my-python
  ];

  shellHook = ''
    export PYTHONPATH="${my-python}/${my-python.sitePackages}:$PYTHONPATH"
    echo "--- Blender Dev Environment Ready ---"
    echo "Blender version: $(blender --version | head -n 1)"
    echo "Python path set to include: ${my-python.sitePackages}"
  '';
}