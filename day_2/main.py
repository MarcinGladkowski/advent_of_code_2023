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


class Cube:

    def __init__(self, color: Color, value: int):
        super().__init__()
        self.color = color
        self.value = value

    @classmethod
    def from_plain(cls, input: str):
        matches = re.search('(\d{1,2})\s{1}(\w+)', input)

        if matches is None:
            raise ValueError(f"Cannot parse cube for input {input}")

        return cls(Color[matches.group(2).upper()], int(matches.group(1)))


class Set:

    def __init__(self, cubes: list):
        self.cubes = [] if cubes is None else cubes

    def add(self, cube: Cube) -> None:
        self.cubes.append(cube)

    def get_by_color(self, color: Color):
        filtered = list(filter(lambda x: x.color.__eq__(color), self.cubes))

        if not filtered:
            raise ValueError(f"Color not found {color.value}")

        return filtered[0]


class RevealSet(Set):
    """
        12 red cubes,
        13 green cubes,
        and 14 blue cubes
    """
    def __init__(self):
        super().__init__()
        self.cubes = [
            Cube(Color.RED, 12),
            Cube(Color.GREEN, 13),
            Cube(Color.BLUE, 14),
        ]

    def is_possible(self, cube: Cube) -> bool:
        pass


def get_game_id(game_title: str):
    result = re.search('\d', game_title)

    if result is None:
        raise ValueError("Problem with GAME ID")

    return result.group(0)


def get_sets(sets: str):
    return sets.split(";")


games = {}
for plain_game in test_data:
    title, cubes = plain_game.split(':')
    game = Game(int(get_game_id(title)), [])

    for set in get_sets(cubes):
        new_set = Set([])
        for cube in set.split(','):
            new_set.add(Cube.from_plain(cube))
        game.sets.append(new_set)


red_6 = Cube.from_plain('6 red')
assert red_6.color == Color.RED
assert red_6.value == 6

test_cube = Set([Cube(Color.RED, 6)])

assert test_cube.get_by_color(Color.RED).value == 6
