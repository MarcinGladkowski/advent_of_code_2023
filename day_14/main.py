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


pivoted = pivot(test_input)  # first pivot
pivoted_second_time = pivot(pivoted)  # second pivot - back to inital state

assert pivoted != test_input
assert pivoted_second_time == test_input


def slide_partial_left_and_north(row: str):
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


def slide_partial_right_and_south(row: str):

    row = row[::-1]
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

    new_row = new_row[::-1]
    return new_row


assert ['.', '.', '.', '.', 'O', 'O', 'O', 'O', '#', '#'] == slide_partial_right_and_south(['O', 'O', '.', 'O', '.', 'O', '.', '.', '#', '#'])
assert ['.', 'O', 'O'] == slide_partial_right_and_south(['O', '.', 'O'])
assert ['O', '#', 'O'] == slide_partial_right_and_south(['O', '#', 'O'])


def slide_row_north_west(row: list) -> list:
    square_rocks_partials = ''.join(row).split('#')
    result = '#'.join([''.join(slide_partial_left_and_north(row)) for row in square_rocks_partials])
    return [_ for _ in result]


def slide_row_south_east(row: list) -> list:
    square_rocks_partials = ''.join(row).split('#')
    result = '#'.join([''.join(slide_partial_right_and_south(row)) for row in square_rocks_partials])
    return [_ for _ in result]


assert (['O', '.', '.', '.', '.', '#', 'O', 'O', '.', '.'] == slide_row_north_west(['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O']))
assert (['O', '.', '.', '.', '#', '#', 'O', 'O', '.', '.'] == slide_row_north_west(['.', '.', 'O', '.', '#', '#', 'O', '.', '.', 'O']))
assert (['.', '.', '.', 'O', '#', '#', '.', '.', 'O', 'O'] == slide_row_south_east(['.', '.', 'O', '.', '#', '#', 'O', '.', '.', 'O']))

def slide_board_north_west(board: list):
    return [slide_row_north_west(row) for row in board]


def slide_board_east_south(board: list):
    return [slide_row_south_east(row) for row in board]


pivot_slide_board = slide_board_north_west(pivot(test_input))


def count_stones_load(board: list) -> int:
    total_load = 0
    for row in board:
        total_load += sum([len(row) - i for i, el in enumerate(row) if el == 'O'])

    return total_load


assert 136 == count_stones_load(pivot_slide_board)

input = load_data('input.txt')
# pivot
data = [[_ for _ in x] for x in input]

pivot_slide_board_data = slide_board_north_west(pivot(data))

assert 109939 == count_stones_load(pivot_slide_board_data)


def get_direction():
    directions = ['north', 'west', 'south', 'east']
    index = 0

    while True:
        if index >= len(directions):
            index = 0

        yield directions[index]
        index += 1


directions = get_direction()
"""Testing generator"""
next(directions)
next(directions)
next(directions)
next(directions)
assert 'north' == next(directions)


class Cycle:
    """
    What is one cycle ?
    initial move - north (requires one pivot)
    pivot -> move north
    pivot ->
    """

    def __init__(self, board: list):
        self.board = board
        self.direction_generator = get_direction()
        self.direction = next(self.direction_generator)
        self.pivot()

    def pivot(self):
        self.board = pivot(self.board)

    def next_direction(self):
        self.direction = next(self.direction_generator)

    def slide(self):
        if self.direction == 'north' or self.direction == 'west':
            self.board = slide_board_north_west(self.board)

        if self.direction == 'south' or self.direction == 'east':
            self.board = slide_board_east_south(self.board)

        self.pivot()
        self.next_direction()


# testing cycle mechanism
test_one_cycle = Cycle(test_input)
test_one_cycle.slide()
test_one_cycle.slide()
test_one_cycle.slide()
test_one_cycle.slide()

# why pivot ? - how to asure that side is right ?
test_one_cycle.pivot()

# test data to compare
test_set_after_one_cycle = [
    ['.', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '#', '.', '.', '.', 'O', '#'],
    ['.', '.', '.', 'O', 'O', '#', '#', '.', '.', '.'],
    ['.', 'O', 'O', '#', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', 'O', 'O', 'O', '#', '.'],
    ['.', 'O', '#', '.', '.', '.', 'O', '#', '.', '#'],
    ['.', '.', '.', '.', 'O', '#', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'O', 'O', 'O', 'O'],
    ['#', '.', '.', '.', 'O', '#', '#', '#', '.', '.'],
    ['#', '.', '.', 'O', 'O', '#', '.', '.', '.', '.'],
]

assert test_one_cycle.board == test_set_after_one_cycle
