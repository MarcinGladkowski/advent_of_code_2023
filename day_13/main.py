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
    Solution based on indexes!

    We have to check two axis as once and get only
    that one which touch an at least one edge.
    """


    # transform data
    pass


def to_columns(data: list):
    rows_length = len(data[0])
    to_columns = [[] for _ in range(rows_length)]

    for i, row in enumerate(data):
        for j, element in enumerate(row):
            to_columns[j].append(element)

    return to_columns


def neighbouring_pairs(board: list) -> list:
    pairs = []
    for i, x in enumerate(board):

        if i + 1 >= len(board):
            continue

        if ''.join(x) == ''.join(board[i + 1]):
            pairs.append((i, i + 1))

    return pairs

def check_vertical(data: list) -> list:
    """
    Firstly we're rewriting columns to rows
    and then returning indexes of found middle columns
    """
    transformed_data = to_columns(data)
    return neighbouring_pairs(transformed_data)


def check_horizontal(data: list) -> list:
    """Returning indexes of found middle columns"""
    return neighbouring_pairs(data)


assert [(3, 4)] == check_horizontal(test_data_horizontal)
assert [(4, 5)] == check_vertical(test_data_vertical)


def is_same(row_a: list, row_b: list) -> bool:
    return ''.join(row_a) == ''.join(row_b)


assert is_same(['.', '#', '.'], ['.', '#', '.'])
assert is_same(['.', '#', '.'], ['.', '#', '#']) == False


def is_mirrored(columns: list, middle: tuple[int, int]) -> bool:
    """
    Columns must be transformed before!
    check rows from middle to edges
    """
    counter_down, counter_up = middle

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


transformed_test_data_vertical = to_columns(test_data_vertical)
assert is_mirrored(transformed_test_data_vertical, (4, 5))

assert is_mirrored(test_data_horizontal, (3, 4)) == True
assert is_mirrored(transformed_test_data_vertical, (2, 3)) == False
assert is_mirrored(transformed_test_data_vertical, (6, 7)) == False
