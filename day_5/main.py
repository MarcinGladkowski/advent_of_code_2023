from shared.main import load_data

test_data = load_data('input_test.txt')
data = load_data('input.txt')

assert '50 98 2'.replace(' ', '').isnumeric()


def is_data_line_numeric(line: str) -> bool:
    return line.replace(' ', '').isnumeric()


def get_operation_name(line: str) -> str:
    return line.replace(' map:', '')


class Range:

    def __init__(self, start: int, step: int):
        self.step = step
        self.start = start

    def in_range(self, test_seed: int):
        if self.start <= test_seed <= self.start + self.step:
            return True

        return False

    def diff_start(self, range) -> bool:
        return range.start - self.start

    def get_as_list(self) -> list:
        return [x for x in range(self.start, self.start+self.step)]

    def __str__(self):
        return f"{self.start} - {self.step}"


class Category:
    def __init__(self, ranges: list[Range] = None):
        self.ranges = [] if ranges is None else ranges

    def get_range(self, index: int):
        return self.ranges[index]

    def add_range(self, range: Range) -> None:
        self.ranges.append(range)


'''
    seed-to-soil solution
    Test for seed 79   
    
    50 98 2
    52 50 48 
'''
base = Category([Range(98, 2), Range(50, 48)])
destination = Category([Range(50, 2), Range(52, 48)])

line_to_parse = '50 98 2'


def get_ranges_from_line(line: str) -> tuple:
    destination_value, base_value, step_value = map(lambda x: int(x), line.split(' '))

    return Range(base_value, step_value), Range(destination_value, step_value)


def calculate_destination(base: Category, destination: Category, test_seed: int) -> int:
    for i, range in enumerate(base.ranges):
        if range.in_range(test_seed):
            # got range
            diff = range.diff_start(destination.get_range(i))

            return test_seed + diff

    return test_seed


assert 81 == calculate_destination(base, destination, 79)
assert 14 == calculate_destination(base, destination, 14)
assert 57 == calculate_destination(base, destination, 55)
assert 13 == calculate_destination(base, destination, 13)


def parse_input(data: list) -> dict:
    operations = {
        'seed-to-soil': {
            'dest': Category(),
            'base': Category()
        },
        'soil-to-fertilizer': {
            'dest': Category(),
            'base': Category()
        },
        'fertilizer-to-water': {
            'dest': Category(),
            'base': Category()
        },
        'water-to-light': {
            'dest': Category(),
            'base': Category()
        },
        'light-to-temperature': {
            'dest': Category(),
            'base': Category()
        },
        'temperature-to-humidity': {
            'dest': Category(),
            'base': Category()
        },
        'humidity-to-location': {
            'dest': Category(),
            'base': Category()
        },
    }
    operation_pointer = None
    for i, line in enumerate(data):

        if line.startswith('seeds'):
            title, seeds = line.split(':')
            operations[title] = list(map(lambda x: int(x), filter(lambda x: x.isnumeric(), seeds.split(' '))))
            continue

        for operation in operations.keys():

            if line.startswith(operation) and operation_pointer is not None:
                operation_pointer = get_operation_name(operation)
                continue

            if line.startswith(operation) and operation_pointer is None:
                operation_pointer = get_operation_name(operation)
                continue

            if is_data_line_numeric(line):
                base, dest = get_ranges_from_line(line)
                operations[operation_pointer]['base'].add_range(base)
                operations[operation_pointer]['dest'].add_range(dest)
                break

    return operations


parsed = parse_input(test_data)


def calculate_seed(destination_to_source: dict, input_seed: int):
    results = []
    input_seed = input_seed
    results.append(input_seed)
    for operation, operation_map in destination_to_source.items():

        if operation == 'seeds':
            continue

        result = calculate_destination(operation_map['base'], operation_map['dest'], input_seed)
        input_seed = result
        results.append(input_seed)

    return results


""" Seed 79 -> soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82."""
assert [79, 81, 81, 81, 74, 78, 78, 82] == calculate_seed(parsed, 79)

"""Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43. """
assert [14, 14, 53, 49, 42, 42, 43, 43] == calculate_seed(parsed, 14)

"""Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86."""
assert [55, 57, 57, 53, 46, 82, 82, 86] == calculate_seed(parsed, 55)

"""Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35."""
assert [13, 13, 52, 41, 34, 34, 35, 35] == calculate_seed(parsed, 13)


def calculate_with_all_seeds(data: list):
    """last number is location, the lowest from all of them"""
    parsed = parse_input(data)

    locations = []
    for seed in parsed['seeds']:
        map_result = calculate_seed(parsed, seed)

        locations.append(map_result[-1])

    return min(locations)


assert 35 == calculate_with_all_seeds(test_data)

print(calculate_with_all_seeds(data))

assert 92 == Range(79, 14).get_as_list()[-1]


def calculate_all_seeds_range(data: list):
    """
        - last number is location, the lowest from all of them
        - get ranges of seeds
    """
    parsed = parse_input(data)

    ranges = []

    for i, seed in enumerate(parsed['seeds']):
        if i == 0 or i % 2 == 0:
            ranges += Range(seed, parsed['seeds'][i+1]).get_as_list()

    locations = []
    for seed in ranges:
        map_result = calculate_seed(parsed, seed)

        locations.append(map_result[-1])

    return min(locations)


assert 46 == calculate_all_seeds_range(test_data)