TEST_DATA_1 = 'input_test_part_1.txt'
TEST_DATA_2 = 'input_test_part_2.txt'
DATA_1 = 'input_part_1.txt'
DATA_2 = 'input_part_2.txt'


def load_data(file_name: str) -> list:
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]


codes = []

test_data = load_data(TEST_DATA_1)


def basic_filter(row) -> list:
    numbers = list(filter(lambda x: x.isnumeric(), row))
    filtered = [n for idx, n in enumerate(numbers) if idx == 0 or idx == len(numbers) - 1]

    return filtered


def keywords_filter(data: list) -> list:
    """From full rows"""
    return list(map(lambda row: parse_with_keywords(row), data))


def calculate_sum(data: list, filter: callable) -> int:
    result_sum = 0

    for row in data:

        filtered = filter(row)

        if len(filtered) == 2:
            result_sum += int(''.join(filtered))

        if len(filtered) == 1:
            result_sum += int(filtered[0] * 2)

    return result_sum


# assert 142 == calculate_sum(test_data, basic_filter)
# print(calculate_sum(load_data(DATA_1), basic_filter)) -> result day 1 - part 1

keywords = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '1', '2', '3', '4', '5', '6', '7',
            '8', '9']

""" DRY! """
numbers_dictionary = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def parse_with_keywords(row: str) -> dict:
    parsed = {}
    for k in keywords:
        found = row.find(k)
        if found != -1:
            parsed[found] = k

    return dict(sorted(parsed.items()))


assert parse_with_keywords('ttfourtwo3') == {2: 'four', 6: 'two', 9: '3'}


def get_number_for_keywords_search(row_result: dict) -> list:
    return list(
        map(lambda x: numbers_dictionary.get(x) if x in list(numbers_dictionary.keys()) else x, row_result.values()))



def calculate_sum_with_keywords(data: list) -> int:
    result_sum = 0

    recognized = list(map(lambda row: parse_with_keywords(row), data))

    parsed = list(map(lambda row: get_number_for_keywords_search(row), recognized))

    for filtered in parsed:

        if len(filtered) > 1:
            result_sum += int(''.join([filtered[0], filtered[-1]]))

        if len(filtered) == 1:
            result_sum += int(filtered[0] * 2)

    return result_sum


assert get_number_for_keywords_search({1: 'two', 3: 'four', 9: '9'}) == ['2', '4', '9']



print(calculate_sum_with_keywords(load_data(TEST_DATA_2)))

#assert 281 == calculate_sum(load_data(TEST_DATA_2), keywords_filter)
