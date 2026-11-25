{self', pkgs, ...}: 
  pkgs.mkShell {
    packages = with pkgs; [
      just
      self'.packages.python
      black
      isort
    ];
  ZK_NOTEBOOK_DIR = "/home/dragon/Documents/Projects/GMAcli/.notes";
}
