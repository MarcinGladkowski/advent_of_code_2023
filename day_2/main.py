from dataclasses import dataclass
import re
from enum import Enum

TEST_DATA_1 = 'input_test.txt'


def load_data(file_name: str) -> list:
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]


test_data = load_data(TEST_DATA_1)


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'glue'


@dataclass
class Game:
    id: int
    sets: list


class Set:

    @classmethod
    def from_string(self, s: str) -> None:
        pass


def get_game_id(game_title: str):
    result = re.search('\d', game_title)

    if result is None:
        raise ValueError("Problem with GAME ID")

    return result.group(0)


def get_sets(sets: str):
    sets = sets.split(";")
    print(sets)


games = {}
for plain_game in test_data:
    title, cubes = plain_game.split(':')

    get_game_id(title)
    get_sets(cubes)


class Cube:

    def __init__(self, color: Color, value: int):
        super().__init__()
        self.color = color
        self.value = value

    @classmethod
    def from_plain(cls, input: str):
        matches = re.search('(\w+)\s{1}(\d{1,2})', input)

        if matches is None:
            raise ValueError("Cannot parse cube")

        return cls(Color[matches.group(1).upper()], int(matches.group(2)))


red_6 = Cube.from_plain('Red 6')

assert red_6.color == Color.RED
assert red_6.value == 6
