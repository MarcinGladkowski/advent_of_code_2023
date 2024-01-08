test_data_vertical = [
    ['#', '.', '#', '#', '.', '.', '#', '#', '.'],
    ['.', '.', '#', '.', '#', '#', '.', '#', '.'],
    ['#', '#', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '#', '.', '.', '.', '.', '.', '.', '#'],
    ['.', '.', '#', '.', '#', '#', '.', '#', '.'],
    ['.', '.', '#', '#', '.', '.', '#', '#', '.'],
    ['#', '.', '#', '.', '#', '#', '.', '#', '.'],
]

test_data_horizontal = [
    ['#', '.', '.', '.', '#', '#', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '#', '.', '.', '#'],
    ['.', '.', '#', '#', '.', '.', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '.', '#', '#', '.'],
    ['#', '#', '#', '#', '#', '.', '#', '#', '.'],
    ['.', '.', '#', '#', '.', '.', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '#', '.', '.', '#']
]


def recognize_axis(board: list):
    pass


def check_vertical(data: list) -> tuple[int, int] | None:
    """
    firstly we're rewriting columns to rows
    """
    rows_length = len(data[0])
    to_columns = [[] for _ in range(rows_length)]

    for i, row in enumerate(data):
        for j, element in enumerate(row):
            to_columns[j].append(element)

    for i, x in enumerate(to_columns):
        if ''.join(x) == ''.join(to_columns[i + 1]):
            return i + 1, i + 2


def check_horizontal(data: list) -> tuple[int, int] | None:
    for i, x in enumerate(data):
        if ''.join(x) == ''.join(data[i + 1]):
            return i + 1, i + 2


assert (4, 5) == check_horizontal(test_data_horizontal)
assert (5, 6) == check_vertical(test_data_vertical)
