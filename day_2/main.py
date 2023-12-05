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
    BLUE = 'blue'

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


