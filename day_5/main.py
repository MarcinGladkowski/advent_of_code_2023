from shared.main import load_data

test_data = load_data('input_test.txt')

sanitize = [x for x in test_data if x != '']

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


class Category:
    def __init__(self, ranges: list[Range] = None):
        self.ranges = ranges

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


def parse_input(data: list) -> list:
    operations = {
        'seed-to-soil': None,
        'soil-to-fertilizer': None,
        'fertilizer-to-water': None,
        'water-to-light': None,
        'light-to-temperature': None,
        'temperature-to-humidity': None,
        'humidity-to-location': None,
    }
    operation_pointer = None
    for i, line in enumerate(data):
        if line.startswith('seeds'):
            """Seeds list parsing"""
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
                print(line)
                break






    print(operations)

parse_input(test_data)