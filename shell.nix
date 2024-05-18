{ pkgs ? import <nixpkgs> {} }:

let
  python-packages = ps: with ps; [
    django
    tensorflow
    keras
    matplotlib
    numpy
    pillow
  ];
  my-python = pkgs.python311.withPackages python-packages;
in
pkgs.mkShell {
  packages = [
    (my-python)
  ];
}
