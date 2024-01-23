from pprint import pprint

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
    pivot_board = [[] for _ in range(len(board[0]))]

    for j, row in enumerate(board):
        for i, x in enumerate(row):
            pivot_board[i].append(x)

    return pivot_board


pivoted = pivot(test_input)


def slide_north(row: list):

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


assert ['O', 'O', 'O', 'O', '.', '.', '.', '.', '#', '#'] == slide_north(['O', 'O', '.', 'O', '.', 'O', '.', '.', '#', '#'])