from dataclasses import dataclass
import re
from enum import Enum

TEST_DATA_1 = 'input_test.txt'
TEST_DATA = 'input.txt'


def load_data(file_name: str) -> list:
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]


test_data = load_data(TEST_DATA_1)
data_part_1 = load_data(TEST_DATA)


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


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

    def __str__(self):
        return f"Cube({self.color.value}, {self.value})"


class Set:

    def __init__(self, cubes: list):
        self.cubes = [] if cubes is None else cubes

    def add(self, cube: Cube) -> None:
        self.cubes.append(cube)

    def get_by_color(self, color: Color):
        filtered = list(filter(lambda x: x.color.value == color.value, self.cubes))

        if not filtered:
            return None

        return filtered[0]

    def __str__(self):
        for cube in self.cubes:
            print(cube.__str__())


class RevealSet(Set):
    """
        12 red cubes,
        13 green cubes,
        and 14 blue cubes
    """

    def __init__(self):
        self.cubes = [
            Cube(Color.RED, 12),
            Cube(Color.GREEN, 13),
            Cube(Color.BLUE, 14),
        ]

    def is_possible(self, set: Set) -> bool:

        for color in self.cubes:
            found_cube = set.get_by_color(color.color)

            if found_cube is None:
                continue

            if color.value < found_cube.value:
                return False

        return True


@dataclass
class Game:
    id: int
    sets: list

    def is_possible(self, reveal_set: RevealSet) -> bool:
        for set in self.sets:
            if reveal_set.is_possible(set) is False:
                return False

        return True

    def __str__(self):
        print("GAME")
        for cube_set in self.sets:
            cube_set.__str__()

    def highest_color(self) -> dict:
        sum_sets_by_color = {
            'green': [],
            'red': [],
            'blue': [],
        }

        for game_set in self.sets:
            for cube in game_set.cubes:
                sum_sets_by_color[cube.color.value].append(cube.value)

        return {
            Color.RED.value: max(sum_sets_by_color[Color.RED.value]),
            Color.GREEN.value: max(sum_sets_by_color[Color.GREEN.value]),
            Color.BLUE.value: max(sum_sets_by_color[Color.BLUE.value]),
        }

    def calculate_colors(self) -> int:

        fewer_colors = self.highest_color()

        return fewer_colors[Color.GREEN.value] * fewer_colors[Color.RED.value] * fewer_colors[Color.BLUE.value]


sum_game = Game(1, [])

set_1 = Set([])
set_2 = Set([])
set_1.add(Cube(Color.GREEN, 10))
set_1.add(Cube(Color.RED, 10))
set_1.add(Cube(Color.BLUE, 10))
set_2.add(Cube(Color.GREEN, 20))
set_2.add(Cube(Color.RED, 40))
set_2.add(Cube(Color.BLUE, 50))
sum_game.sets.append(set_1)
sum_game.sets.append(set_2)

sum_by_colors = sum_game.highest_color()


assert 20 == sum_game.highest_color()[Color.GREEN.value]

def get_game_id(game_title: str):
    result = re.search('\d{1,3}', game_title)

    if result is None:
        raise ValueError("Problem with GAME ID")

    return result.group(0)


def get_sets(sets: str):
    return sets.split(";")


red_6 = Cube.from_plain('6 red')
assert red_6.color == Color.RED
assert red_6.value == 6

test_cube = Set([Cube(Color.RED, 6)])

assert test_cube.get_by_color(Color.RED).value == 6

reveal_set = RevealSet()

set_possible_1 = Set([
    Cube(Color.RED, 11),
    Cube(Color.GREEN, 11),
    Cube(Color.BLUE, 1),
])

set_impossible_1 = Set([
    Cube(Color.RED, 100),
    Cube(Color.GREEN, 11),
    Cube(Color.BLUE, 1),
])

assert reveal_set.is_possible(set_possible_1)
assert reveal_set.is_possible(set_impossible_1) == False


def build_game(test_data: list):
    games = []
    for plain_game in test_data:
        title, cubes = plain_game.split(':')
        game = Game(int(get_game_id(title)), [])

        for set in get_sets(cubes):
            new_set = Set([])
            for cube in set.split(','):
                new_set.add(Cube.from_plain(cube))
            game.sets.append(new_set)

        games.append(game)

    return games


def count_possible_games(games: list) -> int:
    reveal_set = RevealSet()
    result = 0
    for game in games:
        if game.is_possible(reveal_set):
            result += game.id

    return result


def count_power_of_colors(games: list) -> int:
    result = 0
    for game in games:
        result += game.calculate_colors()

    return result

result = count_possible_games(build_game(test_data))
# print(result)
result_data = count_possible_games(build_game(data_part_1))

assert result_data == 1853

assert 72706 == count_power_of_colors(build_game(data_part_1))
