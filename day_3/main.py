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

    @staticmethod
    def is_symbol(char: str) -> bool:
        for symbol in Symbols:
            if char == symbol.value:
                return True

        return False


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} - {self.y}"

    def is_adjacent_symbol(self, schema: list) -> bool:

        for x in schema[self.y-1][self.x-1:self.x+2]: # above line
            if Symbols.is_symbol(x):
                return True

        for x in schema[self.y][self.x-1:self.x+2]: # element line
            if Symbols.is_symbol(x):
                return True

        for x in schema[self.y+1][self.x-1:self.x+2]: # below line\
            if Symbols.is_symbol(x):
                return True

        return False


class SchematicNumber:

    def __init__(self, number: str):
        self.number = number
        self.positions = []
        

part_testing = [
    '....',
    '.63.',
    '#...'
]

test_point = Point(1,1)

assert test_point.is_adjacent_symbol(part_testing)


def get_number_positions(line_index: int, line: str):
    numbers = re.findall(r'\d+', line)

    numbers_positions = []

    for number in numbers:
        
        schematic_number = SchematicNumber(number)

        start = line.find(number)

        for _ in number:
            schematic_number.positions.append(Point(line_index, start))

        numbers_positions.append(schematic_number)

    return numbers_positions


schema_positions = []
for i, line in enumerate(part_testing):

    number_positions = get_number_positions(i, line)

    if number_positions:
        schema_positions.append(number_positions)


# test result = 4361
for line_positions in schema_positions:
    for position in line_positions:
        print(position.number)


def get_numbers_with_symbols(data: list):
    for idx, row in enumerate(data):
        print(row)

get_numbers_with_symbols(test_data)