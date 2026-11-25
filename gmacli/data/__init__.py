import json
import random
from pathlib import Path
from typing import Any

data_path = Path(__file__).resolve().parent


def get_words() -> dict[str, str]:
    words: dict[str, str] = {}
    word_types: list[str] = ["adjectives", "nouns", "verbs"]

    for w_type in word_types:
        words[w_type] = open_data(w_type)

    return words

def get_data(d_type: str) -> Any:
    d_path: Path = data_path / f"{d_type}.json"
    with d_path.open(encoding="utf-8") as file:
        loaded: Any = json.load(file)

    return loaded


def open_data(d_type: str) -> Any:
    d_path: Path = data_path / f"{d_type}.json"
    with d_path.open(encoding="utf-8") as file:
        pool: Any = json.load(file)

    return grab_word(pool)


def grab_word(pool: Any) -> Any:
    return random.choice(pool)

