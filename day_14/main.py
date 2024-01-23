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
    For easiest operating ont
    """
    pivot_board = [[] for _ in range(len(board[0]))]

    for j, row in enumerate(board):
        for i, x in enumerate(row):
            pivot_board[i].append(x)

    return pivot_board


pivoted = pivot(test_input)


def slide_partial(row: list):
    stones_count = len(list(filter(lambda x: x == 'O', row)))

    new_row = []
    for i, el in enumerate(row):
        if i < stones_count:
            new_row.append('O')
            continue
        if el == 'O':
            new_row.append('.')
            continue
        new_row.append(el)

    return new_row


assert ['O', 'O', 'O', 'O', '.', '.', '.', '.', '#', '#'] == slide_partial(
    ['O', 'O', '.', 'O', '.', 'O', '.', '.', '#', '#'])


def slide(row: list) -> list:
    """
    ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O']
    """
    square_rocks_partials = ''.join(row).split('#')  # test if separating rows is more than one ###
    result = '#'.join([''.join(slide_partial(row)) for row in square_rocks_partials])
    return [_ for _ in result]


assert (['O', '.', '.', '.', '.', '#', 'O', 'O', '.', '.']
        == slide(['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O']))

assert (['O', '.', '.', '.', '#', '#', 'O', 'O', '.', '.']
        == slide(['.', '.', 'O', '.', '#', '#', 'O', '.', '.', 'O']))


def slide_board(board: list):
    return [slide(row) for row in board]


pivot_slide_board = slide_board(pivot(test_input))


def count_stones_load(board: list) -> int:
    total_load = 0
    for row in board:
        total_load += sum([len(row) - i for i, el in enumerate(row) if el == 'O'])

    return total_load


assert 136 == count_stones_load(pivot_slide_board)

input = load_data('input.txt')
# pivot
data = [[_ for _ in x] for x in input]

pivot_slide_board_data = slide_board(pivot(data))


assert 109939 == count_stones_load(pivot_slide_board_data)