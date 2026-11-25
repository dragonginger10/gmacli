from typing import Annotated

import typer

from gmacli.dice import dice_set
from gmacli.renderer import render_card

app = typer.Typer()

@app.command()
def cli_app(art: Annotated[bool, typer.Option('--art', '-a')] = False ,dice: Annotated[list[str] | None, typer.Option('--dice', '-d')] = None) -> None:
    rolls = dice_set(dice)

    render_card(rolls, show_symbol = not art)
