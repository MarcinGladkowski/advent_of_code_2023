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

def get_numbers_with_symbols(data: list):

    for idx, row in enumerate(data):
        print(row)

# test result = 4361

get_numbers_with_symbols(test_data)

