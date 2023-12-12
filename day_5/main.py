from shared.main import load_data

test_data = load_data('input_test.txt')

sanitize = [x for x in test_data if x != '']

print(sanitize)


def parse_input(data: list) -> list:
    operations = {
        'seed-to-soil': [],
        'soil-to-fertilizer': [],
        'fertilizer-to-water': [],
        'water-to-light': [],
        'light-to-temperature': [],
        'temperature-to-humidity': [],
        'humidity-to-location': [],
    }
    for line in sanitize:
        if line.startswith('seeds'):
            operations['seeds'] = line


class ComparePlants:
    def __init__(self, name: str):
        self.name = name


class Range:

    def __init__(self, start: int, step: int):
        self.step = step
        self.start = start


range_1 = Range(98, 2)
range_2 = Range(50, 48)
