TEST_DATA_1 = 'input_test_part_1.txt'
DATA_1 = 'input_part_1.txt'


def load_data(file_name: str) -> list:
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]


codes = []

test_data = load_data(TEST_DATA_1)


def calculate_sum(data: list) -> int:
    result_sum = 0

    for x in data:
        numbers = list(filter(lambda x: x.isnumeric(), x))
        filtered = [n for idx, n in enumerate(numbers) if idx == 0 or idx == len(numbers) - 1]

        if len(filtered) == 2:
            result_sum += int(''.join(filtered))

        if len(filtered) == 1:
            result_sum += int(filtered[0] * 2)

    return result_sum


assert 142 == calculate_sum(test_data)

print(calculate_sum(load_data(DATA_1)))
