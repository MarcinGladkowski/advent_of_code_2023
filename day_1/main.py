import re

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


assert 142 == calculate_sum(test_data, basic_filter)

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


def find_numeric_words(row: str, sub_str: str, start: int = 0, found: list = []):
    """
        Returns indexes from found words e.g. [0, 5]
    """
    find = row.find(sub_str, start)

    if start >= len(row):
        return found

    if find == -1:
        start += 1
        return find_numeric_words(row, sub_str, start, found)

    found.append(find)
    start = start + len(sub_str)

    return find_numeric_words(row, sub_str, start, found)


assert find_numeric_words('user2user', 'user', 0, []) == [0, 5]
assert find_numeric_words('m9qvkqlgfhtwo3seven4seven', 'one', 0, []) == []


def parse_with_keywords(row: str) -> dict:
    parsed = {}

    for numeric_word in numbers_dictionary.keys():
        indexes = find_numeric_words(row, numeric_word, 0, [])
        for idx in indexes:
            parsed[idx] = numeric_word


    for k in numbers_dictionary.values():
        for idx, l in enumerate(row):
            if k == l:
                parsed[idx] = l

    return dict(sorted(parsed.items()))



assert parse_with_keywords('m9qvkqlgfhtwo3seven4seven') == {1: '9', 10: 'two', 13: '3', 14: 'seven', 19: '4',
                                                            20: 'seven'}

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
assert 281 == calculate_sum_with_keywords(load_data(TEST_DATA_2))


print("Day_1 - part 2 result: ")
print(
    calculate_sum_with_keywords(load_data(DATA_2))
)

exit()
def test_recognize_data(data: list):
    """
    Test function
    :param data:
    :return:
    """

    recognized = list(map(lambda x: parse_with_keywords(x), data))

    parsed = list(map(lambda row: get_number_for_keywords_search(row), recognized))

    for parse in parsed:
        print(parse)

    with open('decoded.txt', 'w') as f:
        for row in parsed:
            f.write(','.join(map(str, row)) + '\n')


test_recognize_data(load_data(DATA_2))
