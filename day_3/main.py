import re
from enum import Enum

TEST_DATA = 'input_test.txt'


def load_data(file_name: str) -> list:
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]


test_data = load_data(TEST_DATA)


class Symbols(Enum):
    HASHTAG = '#'
    PLUS = '+'
    DOLLAR = '$'
    STAR = '*'


part_testing = [
    ['....'],
    ['.63.'],
    ['#...']
]


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} - {self.y}"


def get_number_positions(line_index: int, line: str):
    numbers = re.findall(r'\d+', line)

    numbers_positions = {}

    for number in numbers:
        numbers_positions[number] = []

        start = line.find(number)

        for _ in number:
            numbers_positions[number].append(Point(line_index, start))

    return numbers_positions


print(get_number_positions(0, '...10..456...'))

def get_numbers_with_symbols(data: list):
    for idx, row in enumerate(data):
        print(row)


# test result = 4361

get_numbers_with_symbols(test_data)
