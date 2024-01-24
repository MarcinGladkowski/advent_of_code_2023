from pprint import pprint

from shared.main import load_data

test_input = [
    ['O', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
    ['O', '.', 'O', 'O', '#', '.', '.', '.', '.', '#'],
    ['.', '.', '.', '.', '.', '#', '#', '.', '.', '.'],
    ['O', 'O', '.', '#', 'O', '.', '.', '.', '.', 'O'],
    ['.', 'O', '.', '.', '.', '.', '.', 'O', '#', '.'],
    ['O', '.', '#', '.', '.', 'O', '.', '#', '.', '#'],
    ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O'],
    ['.', '.', '.', '.', '.', '.', '.', 'O', '.', '.'],
    ['#', '.', '.', '.', '.', '#', '#', '#', '.', '.'],
    ['#', 'O', 'O', '.', '.', '#', '.', '.', '.', '.'],
]


def pivot(board: list) -> list:
    """
        Allows to easy move stones north
        Pivot to horizontal view
    """
    pivot_board = [[] for _ in range(len(board[0]))]

    for j, row in enumerate(board):
        for i, x in enumerate(row):
            pivot_board[i].append(x)

    return pivot_board


pivoted = pivot(test_input) # first pivot
pivoted_second_time = pivot(pivoted) # second pivot - back to inital state

assert pivoted != test_input
assert pivoted_second_time == test_input


def slide_partial_left_and_north(row: list):
    stones_count = list(filter(lambda x: x == 'O', row))

    new_row = []
    for i, el in enumerate(row):
        if el == '#':
            new_row.append('#')
            continue
        if stones_count:
            new_row.append('O')
            stones_count.pop()
            continue
        if el == 'O':
            new_row.append('.')
            continue
        new_row.append(el)

    return new_row


assert ['O', 'O', 'O', 'O', '.', '.', '.', '.', '#', '#'] == slide_partial_left_and_north(['O', 'O', '.', 'O', '.', 'O', '.', '.', '#', '#'])
assert ['#', 'O', 'O', 'O', '.', '.', '.', '.', '#', '#'] == slide_partial_left_and_north(['#', 'O', '.', 'O', '.', 'O', '.', '.', '#', '#'])


def slide_partial_right_and_south(row: list):
    row.reverse()
    stones_count = list(filter(lambda x: x == 'O', row))

    new_row = []
    for i, el in enumerate(row):
        if el == '#':
            new_row.append('#')
            continue
        if stones_count:
            new_row.append('O')
            stones_count.pop()
            continue
        if el == 'O':
            new_row.append('.')
            continue
        new_row.append(el)

    new_row.reverse()
    return new_row


assert ['.', '.', '.', '.', 'O', 'O', 'O', 'O', '#', '#'] == slide_partial_right_and_south(['O', 'O', '.', 'O', '.', 'O', '.', '.', '#', '#'])

def slide(row: list) -> list:
    """
    ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O']
    """
    square_rocks_partials = ''.join(row).split('#')  # test if separating rows is more than one ###
    result = '#'.join([''.join(slide_partial_left_and_north(row)) for row in square_rocks_partials])
    return [_ for _ in result]


assert (['O', '.', '.', '.', '.', '#', 'O', 'O', '.', '.']
        == slide(['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O']))

assert (['O', '.', '.', '.', '#', '#', 'O', 'O', '.', '.']
        == slide(['.', '.', 'O', '.', '#', '#', 'O', '.', '.', 'O']))


def slide_board_north(board: list):
    return [slide(row) for row in board]


pivot_slide_board = slide_board_north(pivot(test_input))


def count_stones_load(board: list) -> int:
    total_load = 0
    for row in board:
        total_load += sum([len(row) - i for i, el in enumerate(row) if el == 'O'])

    return total_load


assert 136 == count_stones_load(pivot_slide_board)


input = load_data('input.txt')
# pivot
data = [[_ for _ in x] for x in input]

pivot_slide_board_data = slide_board_north(pivot(data))

assert 109939 == count_stones_load(pivot_slide_board_data)
