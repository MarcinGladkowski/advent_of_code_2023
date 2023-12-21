from shared.main import load_data

test_input = [
    0, 3, 6, 9, 12, 15,
    1, 3, 6, 10, 15, 21,
    10, 13, 16, 21, 30, 45,
]


def get_next_row(row: list) -> list:
    """
        Return next row with one element less len(row) - 6 return 5
    """
    new_row = []
    for i, element in enumerate(row):
        if i + 1 == len(row):
            return new_row

        new_row.append(row[i + 1] - row[i])


assert [2, 3, 4, 5, 6] == get_next_row([1, 3, 6, 10, 15, 21])
assert [0, 0] == get_next_row([1, 1, 1])


def are_only_zeros(row: list) -> bool:
    return len(list(filter(lambda x: x == 0, row))) == len(row)


assert are_only_zeros([0, 0, 0])
assert are_only_zeros([0, 0, 1]) == False
assert are_only_zeros([-1, 0, 1]) == False


def get_extrapolate_value(bottom: list, up: list):
    return bottom[-1] + up[-1]


def add_extrapolate(value: int, up: list):
    return up.append(value)


def extrapolate(up: list, bottom: list) -> tuple:
    value = get_extrapolate_value(bottom, up)
    add_extrapolate(value, up)
    return up, bottom


def generate_rows(row: list) -> list:
    row_map = [row]
    row_map = generate_row_recursion(row_map, row)

    return row_map


def generate_row_recursion(row_map: list, row: list) -> list:
    next_row = get_next_row(row)
    row_map.append(next_row)
    if are_only_zeros(next_row):
        return row_map

    return generate_row_recursion(row_map, next_row)


assert generate_rows([0, 3, 6, 9, 12, 15]) == [
    [0, 3, 6, 9, 12, 15],
    [3, 3, 3, 3, 3],
    [0, 0, 0, 0],
]

assert generate_rows([10, 13, 16, 21, 30, 45]) == [
    [10, 13, 16, 21, 30, 45],
    [3, 3, 5, 9, 15],
    [0, 2, 4, 6],
    [2, 2, 2],
    [0, 0]
]


def extrapolate_map(map: list):
    """
        from bottom to up
        index 0 = list on top
    """
    for i in reversed(range(0, len(map))):
        if i == 0:
            return map

        up = map[i - 1]
        bottom = map[i]

        up, bottom = extrapolate(up, bottom)

        map[i - 1] = up
        map[i] = bottom

        if i == len(map) - 1:
            map[len(map) - 1].append(0)

    return map


assert extrapolate_map(
    [
        [10, 13, 16, 21, 30, 45],
        [3, 3, 5, 9, 15],
        [0, 2, 4, 6],
        [2, 2, 2],
        [0, 0]
    ]
) == [
           [10, 13, 16, 21, 30, 45, 68],
           [3, 3, 5, 9, 15, 23],
           [0, 2, 4, 6, 8],
           [2, 2, 2, 2],
           [0, 0, 0]
       ]


def calculate(data: list) -> int:
    result = 0
    print(f"\n")
    for i, row in enumerate(data):
        row_map = generate_rows(row)
        extrapolated_map = extrapolate_map(row_map)
        last_extrapolated_number = extrapolated_map[0][-1]
        result += last_extrapolated_number  # last element top row

    return result


assert 114 == calculate([
    [0, 3, 6, 9, 12, 15],
    [1, 3, 6, 10, 15, 21],
    [10, 13, 16, 21, 30, 45],
])


def parse_to_lists(data: list) -> list:
    parsed = []
    for row_part_1 in data:
        parsed.append(
            list(map(lambda el: int(el), row_part_1.split(' ')))
        )

    return parsed


part_1_data = parse_to_lists(load_data("input.txt"))

assert 1901217887 == calculate(part_1_data)

"""part 2"""


def extrapolate_map_from_begging(generated_map: list) -> list:
    for i in reversed(range(0, len(generated_map))):
        if i == 0:
            return generated_map

        if i == len(generated_map) - 1:
            """Set zero in front of last row"""
            generated_map[len(generated_map) - 1].insert(0, 0)

        up = generated_map[i - 1]
        bottom = generated_map[i]

        up, bottom = extrapolate_first_element(up, bottom)

        generated_map[i - 1] = up
        generated_map[i] = bottom

    return generated_map


def get_extrapolate_for_first_value(bottom: list, up: list):
    return up[0] - bottom[0]


def add_extrapolate_on_first_index(value: int, up: list):
    up.insert(0, value)
    return up


assert [0, 1, 2, 3] == add_extrapolate_on_first_index(0, [1, 2, 3])


def extrapolate_first_element(up: list, bottom: list) -> tuple:
    value = get_extrapolate_for_first_value(bottom, up)
    add_extrapolate_on_first_index(value, up)
    return up, bottom


row_3 = generate_rows([10, 13, 16, 21, 30, 45]) == [
    [10, 13, 16, 21, 30, 45],
    [3, 3, 5, 9, 15],
    [0, 2, 4, 6],
    [2, 2, 2],
    [0, 0]
]

assert extrapolate_map_from_begging([[10, 13, 16, 21, 30, 45], [3, 3, 5, 9, 15], [0, 2, 4, 6], [2, 2, 2], [0, 0]]) == [[5, 10, 13, 16, 21, 30, 45],[5, 3, 3, 5, 9, 15],[-2, 0, 2, 4, 6],[2, 2, 2, 2],[0, 0, 0]]


def calculate_with_pre_extrapolation(data: list) -> int:
    result = 0
    for i, row in enumerate(data):
        row_map = generate_rows(row)
        extrapolated_map = extrapolate_map_from_begging(row_map)
        last_extrapolated_number = extrapolated_map[0][0]
        result += last_extrapolated_number  # last element top row

    return result


assert 2 == calculate_with_pre_extrapolation([
    [0, 3, 6, 9, 12, 15],
    [1, 3, 6, 10, 15, 21],
    [10, 13, 16, 21, 30, 45],
])

part_1_data = parse_to_lists(load_data("input.txt"))

assert 905 == calculate_with_pre_extrapolation(part_1_data)