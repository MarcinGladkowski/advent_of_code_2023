from pprint import pprint

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
    """
    we have to check two axis as once and get only
    that one which touch an at least one edge.
    """
    pass


def to_columns(data: list):
    rows_length = len(data[0])
    to_columns = [[] for _ in range(rows_length)]

    for i, row in enumerate(data):
        for j, element in enumerate(row):
            to_columns[j].append(element)

    return to_columns


def check_vertical(data: list) -> tuple[int, int] | None:
    """
    Firstly we're rewriting columns to rows
    and then returning indexes of found middle columns
    """
    transformed_data = to_columns(data)

    for i, x in enumerate(transformed_data):
        if ''.join(x) == ''.join(transformed_data[i + 1]):
            return i, i + 1


def check_horizontal(data: list) -> tuple[int, int] | None:
    """Returning indexes of found middle columns"""
    for i, x in enumerate(data):
        if ''.join(x) == ''.join(data[i + 1]):
            return i, i + 1


assert (3, 4) == check_horizontal(test_data_horizontal)
assert (4, 5) == check_vertical(test_data_vertical)


def is_same(row_a: list, row_b: list) -> bool:
    return ''.join(row_a) == ''.join(row_b)


assert is_same(['.', '#', '.'], ['.', '#', '.'])
assert is_same(['.', '#', '.'], ['.', '#', '#']) == False


def is_vertical_mirrored(columns: list, middle: tuple[int, int]) -> bool:
    """
    Columns must be transformed before!
    check rows from middle to edges
    """
    counter_down, counter_up = middle
    counter_up -= 1
    counter_down -= 1

    for i in range(counter_down):
        row_left = counter_down - i
        row_right = counter_up + i

        try:
            left_column = columns[row_left]
            right_column = columns[row_right]
        except:
            return True

        rows_are_same = is_same(left_column, right_column)

        if rows_are_same is False:
            return False

    return True


transformed_data = to_columns(test_data_vertical)
assert is_vertical_mirrored(transformed_data, (5, 6))
