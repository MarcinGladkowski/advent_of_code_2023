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

"""Only absolute differences ?"""

def are_only_zeros(row: list) -> bool:
    return sum(row) == 0


assert are_only_zeros([0, 0, 0])
assert are_only_zeros([0, 0, 1]) == False


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
        try:
            up, bottom = extrapolate(up, bottom)
        except IndexError:
            print("Index out of range")

        map[i - 1] = up
        map[i] = bottom

        """line on bottom with zeroes will fill with additional 0"""
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
    for row in data:
        row_map = generate_rows(row)
        extrapolated_map = extrapolate_map(row_map)
        last_extrapolated_number = extrapolated_map[0][-1]
        print(last_extrapolated_number)
        result += last_extrapolated_number  # last element top row

    return result


assert 114 == calculate([
    [0, 3, 6, 9, 12, 15],
    [1, 3, 6, 10, 15, 21],
    [10, 13, 16, 21, 30, 45],
])

first_rows_generations = generate_rows(
    [-3, 8, 35, 82, 152, 255, 432, 803, 1648, 3531, 7478, 15221, 29521, 54584, 96585, 164316, 269975, 430114, 666765,
     1008764, 1493294
     ])

for row in first_rows_generations:
    print(row)

exit()

part_1_data = load_data("input.txt")


def parse_to_lists(data: list) -> list:
    parsed = []
    for row_part_1 in data:
        parsed.append(
            list(map(lambda el: int(el), row_part_1.split(' ')))
        )

    return parsed

"""
too low: 1901217886
too high: 1904764779
"""
print(calculate(parse_to_lists(part_1_data)))