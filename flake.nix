{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-26.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = ["x86_64-linux" "aarch64-linux"];

      perSystem = {pkgs, self', lib, ...}: {
        devShells.default = import ./.nix/shell.nix {inherit self' pkgs; };
        packages = import ./.nix/package.nix {inherit self' pkgs lib; };
      };
    };
}
