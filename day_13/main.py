import logging
from pprint import pprint
from typing import Tuple, Any

from shared.main import load_data

logging.basicConfig(level=logging.DEBUG)

data = load_data('input.txt')


def generate_boards(raw_data):
    boards = []

    next_board = []
    for i, row in enumerate(raw_data):
        """
            Added two \\n at the input data
            Needs to check when the file is ending
        """
        if row == '':
            boards.append(next_board)
            next_board = []
            continue

        next_board.append([x for x in row])

    return boards


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
    return neighbouring_pairs(data)


def check_horizontal(data: list) -> list:
    """Returning indexes of found middle columns"""
    return neighbouring_pairs(data)


assert [(3, 4)] == check_horizontal(test_data_horizontal)

transformed_test_data_vertical = to_columns(test_data_vertical)

assert [(4, 5)] == check_vertical(transformed_test_data_vertical)


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

    for i in range(counter_down + 1):
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


def recognize_axis(board: list):
    """
    Solution based on indexes!

    We have to check two axis as once and get only
    that one which touch an at least one edge.
    """
    # transform data (for vertical testing)
    # get all middle axis
    # test all axis for mirrors vertical
    # while find mirror return number
    transformed_to_vertical_test = to_columns(board)

    axis_for_vertical = check_vertical(transformed_to_vertical_test)

    axis = {
        'VERTICAL': 0,
        'HORIZONTAL': 0,
    }

    if len(axis_for_vertical) > 0:
        for axle in axis_for_vertical:
            if is_mirrored(transformed_to_vertical_test, axle):
                axis['VERTICAL'] = axle[0] + 1
                break

    # test all axis for mirrors horizontal
    # while find mirror return number
    axis_for_horizontal = check_horizontal(board)

    if len(axis_for_horizontal) > 0:
        for axle in axis_for_horizontal:
            if is_mirrored(board, axle):
                axis['HORIZONTAL'] = (axle[0] + 1) * 100
                break

    type = ''
    result = 0

    for key, value in axis.items():
        result += value
        type += '| ' + key

    return result, ''


assert 5 == recognize_axis(test_data_vertical)[0]
assert 400 == recognize_axis(test_data_horizontal)[0]


def write_processed_board(handler: Any, board: list, metadata: str):
    """mark axle on board and write to file"""
    handler.write('\n')
    handler.write(metadata + '\n')
    for row in board:
        handler.write(''.join(row) + '\n')
    handler.write('\n')


def calculate_sum(boards: list) -> int:
    f = open("debug.txt", "w")
    result = 0
    for i, board in enumerate(boards):
        mirror_result, recognized_mirroring = recognize_axis(board)

        msg = f"board int: {i} | result: {mirror_result} | type: {recognized_mirroring}"

        logging.debug(msg)

        write_processed_board(f, board, msg)

        result += mirror_result

    return result


assert 405 == calculate_sum([test_data_vertical, test_data_horizontal])

input_data = generate_boards(data)
assert 33520 == calculate_sum(input_data) # part 1
