import random

from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from gmacli.data import get_data, get_words, open_data
from gmacli.dice import Rolls, roll_difficulty, roll_likely_odds, roll_tags, scatter_die

ELEMENT_STYLES = {"Air": "bold white", "Fire": "bold red",
                  "Earth": "bold green", "Water": "bold blue"}

ANSWER_STYLES = {"Yes!": "bold bright_green", "Yes": "green",
             "No": "red", "No!": "bold bright_red"}

SENSE_LABELS = {"see": "SEE", "hear": "HEAR", "feel": "FEEL", "smell_taste": "SMELL/TASTE"}

def render_card(
    dice: Rolls, 
    *,
    show_symbol:bool = True,
) -> None:
    console = Console()

    # Words: labels on the first line, results directly below.
    verbs, adjectives, nouns = (get_words()[k] for k in ("verbs", "adjectives", "nouns"))
    console.print(labeled_row(("VERB", "ADJECTIVE", "NOUN"), (verbs, adjectives, nouns), "bold cyan"))
    console.print()

    location = random.choice(get_data("locations"))
    catalyst = random.choice(get_data("catalysts"))
    scene_row = Table(box=None, expand=True, padding=(0, 1))
    scene_row.add_column("LOCATION", justify="center", ratio=1, header_style="bold yellow")
    scene_row.add_column("CATALYST", justify="center", ratio=1, header_style="bold red")
    scene_row.add_row(
        Text(location, style="bold"),
        Text(catalyst, style="italic"),
    )

    console.print(scene_row)
    console.print()

    # Symbol Tags
    tags = roll_tags()
    tag_line = Text("     ").join(
        Text.assemble((icon, ""), " ", (name, "bold")) for icon, name in tags
    )
    console.print(Align.center(tag_line))
    console.print()

    # Names: random names 
    names = get_data("names")
    male, female, neutral = (random.choice(names[k]) for k in ("male", "female", "neutral"))
    console.print(labeled_row(("MALE", "FEMALE", "NEUTRAL"), (male, female, neutral), "bold green"))
    console.print()

    # virtue & vice
    virtue_vices = get_data("virtues_vices")
    virtue, vice = (random.choice(virtue_vices[k]) for k in ("virtues", "vices"))
    traits_row = Table(box=None, expand=True, padding=(0, 1))
    traits_row.add_column("VIRTUE", justify="center", ratio=1, header_style="bold green")
    traits_row.add_column("VICE", justify="center", ratio=1, header_style="bold red")
    traits_row.add_row(
        Text(virtue, style="green"),
        Text(vice, style="red"),
    )

    console.print(traits_row)

    console.print()

    # Belongings
    belongings = get_data("belongings")
    belonging = random.choice(belongings)
    belonging_text = Text.assemble(
        (belonging["type"], "bold"),
        (" — ", "dim"),
        (" · ".join(belonging["examples"]), "dim italic"),
    )

    console.print(Align.center(Text("BELONGING", style="bold blue")))
    console.print(Align.center(belonging_text))
    console.print()

    # sensory lines

    senses = get_data("senses")
    sensory = {sense: random.choice(lines) for sense, lines in senses.items()}
    senses_table = Table.grid(padding=(0, 2))
    senses_table.add_column(style="bold magenta", no_wrap=True)
    senses_table.add_column()
    for key, label in SENSE_LABELS.items():
        senses_table.add_row(label, sensory[key])

    console.print(Align.center(senses_table))
    console.print()


    # Dice: fixed ordering, with every roll shown under its die.
    dice_order = ("d4", "d6", "d8", "d10", "d12", "d20", "d100")
    available_dice = [die for die in dice_order if die in dice]

    if available_dice:
        dice_table = Table(
            box=None,
            expand=True,
            padding=(0, 1),
            header_style="bold yellow",
        )

        for die in available_dice:
            dice_table.add_column(die, justify="center", ratio=1)

        dice_table.add_row(
            *[
                Text(", ".join(str(roll) for roll in dice[die]))
                for die in available_dice
            ]
        )

        console.print(dice_table)
        console.print()


    # Difficulty and scatter die
    diff = roll_difficulty()
    quick = Table.grid(expand=True)
    symbol, label = scatter_die()
    quick.add_column(justify="center", ratio=1)
    quick.add_column(justify="center", ratio=1)
    quick.add_row(
        Text(f"Difficulty: {diff} / 10", style="bold yellow"),
        Text(f"Scatter: {symbol} {label}", style="bold magenta"),
    )
    console.print(quick)
    console.print()

    likely_odds = roll_likely_odds()
    odds_row = Table(box=None, expand=True, padding=(0, 1), header_style="bold")
    for label, chance, _ in likely_odds:
        odds_row.add_column(f"{label} {chance}%", justify="center", ratio=1)

    odds_row.add_row(*(Text(answer, style=ANSWER_STYLES[answer])
                       for _, _, answer in likely_odds))

    console.print(odds_row)
    console.print()

    #rune and element artwork
    rune = open_data("runes")
    element = open_data("elements")
    rune_style = "bold cyan"
    element_style = ELEMENT_STYLES[element["name"]]

    if show_symbol:
        rune_block = art_block(rune["art"], f"{rune['symbol']} {rune['name']}", rune_style)
    else:
        rune_block = Text(rune["name"].upper(), style=rune_style)

    art_row = Table.grid(expand=True, padding=(0, 4))
    art_row.add_column(justify="center", vertical="middle", ratio=1)
    art_row.add_column(justify="center", vertical="middle", ratio=1)
    art_row.add_row(
        rune_block,
        art_block(element["art"], element["name"], element_style),
    )

    console.print(art_row)
    console.print()


    # Interpretation: wrapping text inside a centered box.
    interpretation = Panel(
        Text(rune["interpretation"]),
        title="Interpretation",
        border_style="cyan",
        padding=(1, 2),
        width=min(console.width, 72),
    )

    console.print(Align.center(interpretation)) 


def art_block(art_lines, label, style):
    return Group(
        Text("\n".join(art_lines), style=style, no_wrap=True),
        Text(label.upper(), style=style, justify="center"),
    )

def labeled_row(labels, values, header_style):
    table = Table(box=None, expand=True, padding=(0, 1), header_style=header_style)
    for label in labels:
        table.add_column(label, justify="center", ratio=1)
    table.add_row(*(Text(v, style="bold") for v in values))
    return table
