import re

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

    @staticmethod
    def is_number(char: str):
        return char.isnumeric()


class Point:

    def __init__(self, x: int, y: int, value: str = None):
        self.x = x
        self.y = y
        self.value = value

    def __str__(self):
        return f"{self.x} - {self.y} - {self.value}"

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

    def count_collisions_with_numbers(self, schema: list) -> list:

        start_point = self.x - 1 if self.x - 1 > -1 else 0

        collisions_points = []

        try:
            if self.y - 1 < 0:
                raise IndexError

            if self.x + 1 > len(schema[self.y - 1]):
                raise IndexError

            for i, x in enumerate(schema[self.y - 1][start_point:self.x + 2]):  # above line
                if Symbols.is_number(x):
                    collisions_points.append(Point(i+start_point, self.y-1, x))
        except IndexError:
            pass

        try:
            for i, x in enumerate(schema[self.y][start_point:self.x + 2]):  # element line
                if Symbols.is_number(x):
                    collisions_points.append(Point(i+start_point, self.y, x))
        except IndexError:
            pass

        try:
            for i, x in enumerate(schema[self.y + 1][start_point:self.x + 2]):  # below line
                if Symbols.is_number(x):
                    collisions_points.append(Point(i+start_point, self.y+1, x))
        except IndexError:
            pass

        return collisions_points


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

part_testing_on_single_number = [
    '....',
    '.6..',
    '#...'
]

test_point_single_number = Point(1, 1)

assert test_point_single_number.is_adjacent_symbol(part_testing)


def find_all_numbers(value: str):
    return re.findall(r'\d+', value)


def find_all_gears(value: str):
    return re.findall(r'\*', value)


assert 2 == len(find_all_gears('....*...*'))


def get_number_positions(finder: callable, line_index: int, line: str):
    numbers = finder(line)
    numbers_positions = []
    start_position = 0
    for number in numbers:
        schematic_number = SchematicNumber(number)
        start = line.find(number, start_position)

        for i, _ in enumerate(number):
            schematic_number.positions.append(Point(start + i, line_index))

        start_position = start + len(number)
        numbers_positions.append(schematic_number)

    return numbers_positions


testing_index_search = get_number_positions(find_all_numbers, 0, '.896..6..')

assert testing_index_search[0].number == '896'
assert testing_index_search[1].number == '6'

assert testing_index_search[1].positions[0].x == 6
assert testing_index_search[1].positions[0].y == 0


def parse_to_get_positions(finder: callable, data: list) -> list:
    schema_positions = []
    for i, line in enumerate(data):
        number_positions = get_number_positions(finder, i, line)
        if number_positions:
            schema_positions.extend(number_positions)

    return schema_positions


# test result = 4361
def calculate_numbers_with_symbols(data: list):
    numbers = parse_to_get_positions(find_all_numbers, data)
    total = 0
    for number in numbers:

        result = list(filter(lambda item: item.is_adjacent_symbol(data) is True, number.positions))

        if result:
            total += int(number.number)

    return total


assert 4361 == calculate_numbers_with_symbols(test_data)
assert 527144 == calculate_numbers_with_symbols(data)

"""
Get gears * and theirs positions
"""
gears_positions = parse_to_get_positions(find_all_gears, test_data)

for gear in gears_positions:
    for point in gear.positions:
        collisions = point.count_collisions_with_numbers(test_data)

        if collisions:
            for point in collisions:
                print(point)
