import random
import re

type Rolls = dict[str, list[int]]

TAG_SYMBOLS = [
    ("👑", "Power"),
    ("💀", "Death"),
    ("💰", "Wealth"),
    ("🔑", "Secret"),
    ("🏹", "Conflict"),
    ("🎭", "Deception"),
    ("📜", "Knowledge"),
    ("🌙", "Mystery"),
    ("🔥", "Danger"),
    ("💔", "Loss"),
    ("🐉", "Monster"),
    ("🌲", "Nature"),
]



def roll(sides: int, count: int = 1) -> list[int]:
    return [random.randint(1, sides) for _ in range(count)]


def dice_set(dice: list[str] | None) -> Rolls:
    mask = r"\dd\d"
    rolls: Rolls = {}

    if not dice:
        die = [4, 6, 8, 10, 12, 20, 100]
        for d in die:
            rolls[f"d{d}"] = roll(d)

        return rolls

    for d in dice: 
        if not re.match(mask, d):
            raise ValueError(f"dice option {d} is not valid. Option must be in '#d#' format.")
        count, sides = map(int, d.split('d'))
        rolls[f"d{sides}"] = roll(sides, count)

    return rolls


def scatter_die() -> tuple[str, str]:
    scatter_faces = [
        ("↑", "North"),
        ("↗", "North-East"),
        ("→", "East"),
        ("↘", "South-East"),
        ("↓", "South"),
        ("↙", "South-West"),
        ("←", "West"),
        ("↖", "North-West"),
        ("★", "Crit"),
        ("—", "Miss"),
    ]

    return random.choice(scatter_faces)

def roll_difficulty() -> int:
    diff_vals = list(range(1, 11))
    diff_weights = [
        1,   # 1:   1%
        4,   # 2:   4%
        10,  # 3:  10%
        15,  # 4:  15%
        20,  # 5:  20%
        20,  # 6:  20%
        15,  # 7:  15%
        10,  # 8:  10%
        4,   # 9:   4%
        1,   # 10:  1%
    ]
    return random.choices(
        diff_vals,
        weights=diff_weights,
        k=1,
    )[0]


def ask_oracle(yes_chance: int) -> str:
    roll = random.randint(1, 100)
    if roll <= yes_chance:
        return "Yes!" if roll <= yes_chance / 5 else "Yes"
    no_chance = 100 - yes_chance
    return "No!" if roll > 100 - no_chance / 5 else "No"


def roll_likely_odds(unlikely: int = 25, even: int = 50, likely: int = 75) -> list[tuple[str, int, str]]:
    odds: list[tuple[str, int]] = [('Unlikely', unlikely), ('Even', even), ('Likely', likely)]
    return [(label, chance, ask_oracle(chance)) for label, chance in odds]

def roll_tags(count=3):
    return random.sample(TAG_SYMBOLS, count)
