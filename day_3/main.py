import re
from enum import Enum

TEST_DATA = 'input_test.txt'
DATA = 'input.txt'


def load_data(file_name: str) -> list:
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]


test_data = load_data(TEST_DATA)
data = load_data(DATA)


class Symbols:

    @staticmethod
    def is_symbol(char: str) -> bool:
        if char.isnumeric() or char == '.':
            return False
        return True


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} - {self.y}"

    def is_adjacent_symbol(self, schema: list):

        start_point = self.x - 1 if self.x - 1 > -1 else 0

        neighbors = [[], [], []]

        try:
            if self.y - 1 < 0:
                raise IndexError

            if self.x + 1 > len(schema[self.y - 1]):
                raise IndexError

            for x in schema[self.y - 1][start_point:self.x + 2]:  # above line
                # dump
                neighbors[0].append(x)

                if Symbols.is_symbol(x):
                    return True
        except IndexError:
            pass

        try:
            for x in schema[self.y][start_point:self.x + 2]:  # element line
                neighbors[1].append(x)
                if Symbols.is_symbol(x):
                    return True
        except IndexError:
            pass

        try:
            for x in schema[self.y + 1][start_point:self.x + 2]:  # below line
                neighbors[2].append(x)
                if Symbols.is_symbol(x):
                    return True
        except IndexError:
            pass

        return neighbors


class SchematicNumber:

    def __init__(self, number: str):
        self.number = number
        self.positions = []

    def position(self) -> Point:
        return Point(self.positions[0], self.positions[-1])


part_testing = [
    '....',
    '.63.',
    '#...'
]

test_point = Point(1, 1)

assert test_point.is_adjacent_symbol(part_testing)


def get_number_positions(line_index: int, line: str):
    numbers = re.findall(r'\d+', line)

    numbers_positions = []

    for number in numbers:

        schematic_number = SchematicNumber(number)

        start = line.find(number)

        for i, _ in enumerate(number):
            schematic_number.positions.append(Point(start + i, line_index))

        numbers_positions.append(schematic_number)

    return numbers_positions


def parse_to_get_positions(data: list) -> list:
    schema_positions = []
    for i, line in enumerate(data):

        number_positions = get_number_positions(i, line)

        if number_positions:
            schema_positions.extend(number_positions)

    return schema_positions


# test result = 4361
def get_numbers_with_symbols(data: list):
    numbers = parse_to_get_positions(data)

    all_numbers = []
    not_found = []
    found = []
    total = 0
    for number in numbers:
        all_numbers.append(int(number.number))
        result = list(filter(lambda item: item.is_adjacent_symbol(data) is True, number.positions))

        if result:
            total += int(number.number)
            found.append(int(number.number))
        else:
            not_found.append(int(number.number))
            print(f"Not found number {number.number} at position {number.position()}")

            points_results = list(map(lambda item: item.is_adjacent_symbol(data), number.positions))
            for line in points_results:
                print(line)


    assert len(found) + len(not_found) == len(numbers)

    print(sum(found))
    print(sum(not_found))
    print(sum(all_numbers))

    return total


# assert 4361 == get_numbers_with_symbols(test_data)

# to low 527116, incorrect 587052
print(get_numbers_with_symbols(data))
