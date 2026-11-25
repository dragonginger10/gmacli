{self', pkgs, lib }: {
  default = self'.packages.gmacli;
  python = pkgs.python314.withPackages(p: with p; [
    typer
  ]);

  gmacli = pkgs.python314Packages.buildPythonApplication {
    pname = "gmacli";
    version = "0.1.0";
    src = ./..;
    pyproject = true;

    build-system = with pkgs.python314Packages; [ setuptools ];

    dependencies = with pkgs.python314Packages; [
      typer
    ];

    meta = {
      description = "GameMaster's Apprentice CLI";
      homepage = "";
      license = lib.licenses.gpl3;
      maintainers = with lib.maintainers; [ dragonginger ];
    };
  };
}
