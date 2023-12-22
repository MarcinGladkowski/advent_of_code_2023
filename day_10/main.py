from enum import Enum


class Pipe(Enum):
    NORTH_SOUTH = '|'
    EAST_WEST = '-'
    NORTH_EAST = 'L'
    NORTH_WEST = 'J'
    SOUTH_WEST = '7'
    SOUTH_EAST = 'F'

    @classmethod
    def is_pipe_element(cls, value):
        for element in cls:
            if element.value == value:
                return cls(value)

        return False


assert False == Pipe.is_pipe_element('x')
assert Pipe.EAST_WEST == Pipe.is_pipe_element('-')


class Direction(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    WEST = 'west'
    EAST = 'east'


STARTING_POINT = 'S'
GROUND = '.'

pipe_paths_map = {
    Pipe.NORTH_SOUTH: {
        Direction.NORTH: [Pipe.SOUTH_EAST, Pipe.SOUTH_WEST, Pipe.NORTH_SOUTH],
        Direction.SOUTH: [Pipe.NORTH_EAST, Pipe.NORTH_WEST, Pipe.NORTH_SOUTH]
    },
    Pipe.EAST_WEST: {
        Direction.WEST: [Pipe.EAST_WEST, Pipe.SOUTH_EAST, Pipe.NORTH_EAST],
        Direction.EAST: [Pipe.EAST_WEST, Pipe.NORTH_WEST, Pipe.SOUTH_WEST]
    },
    Pipe.NORTH_EAST: {
        Direction.NORTH: [Pipe.NORTH_SOUTH, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST],
        Direction.EAST: [Pipe.EAST_WEST, Pipe.NORTH_WEST, Pipe.SOUTH_WEST]
    },
    Pipe.NORTH_WEST: {
        Direction.NORTH: [Pipe.NORTH_SOUTH, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST],
        Direction.WEST: [Pipe.EAST_WEST, Pipe.NORTH_EAST, Pipe.SOUTH_EAST]
    },
    Pipe.SOUTH_WEST: {
        Direction.SOUTH: [Pipe.NORTH_SOUTH, Pipe.NORTH_EAST, Pipe.NORTH_WEST],
        Direction.WEST: [Pipe.SOUTH_WEST, Pipe.SOUTH_EAST, Pipe.NORTH_EAST],
    },
    Pipe.SOUTH_EAST: {
        Direction.SOUTH: [Pipe.NORTH_SOUTH, Pipe.NORTH_EAST, Pipe.NORTH_WEST],
        Direction.EAST: [Pipe.EAST_WEST, Pipe.SOUTH_WEST, Pipe.NORTH_WEST]
    }
}

test_map_1 = [
    ['-', 'L', '|', 'F', '7'],
    ['7', 'S', '-', '7', '|'],
    ['L', '|', '7', '|', '|'],
    ['-', 'L', '-', 'J', '|'],
    ['L', '|', '-', 'J', 'F']
]


class PipeElement:

    def __init__(self, y: int, x: int, type: Pipe) -> None:
        self.type = type
        self.y = y
        self.x = x


class Path:

    def __init__(self):
        self.path = []

    def next(self, pipe_element: PipeElement) -> None:
        self.path.append(pipe_element)

    def pointer(self):
        """
        Last element in path is a pointer/position
        """
        return self.path[-1]


'''
Check neighbors to choose correct movement or break path.

Test of element y, x => (1, 2) => '-'
'''
movements = {
    Direction.EAST: lambda element, area: (area[element.y][element.x + 1], element.y, element.x+1),
    Direction.WEST: lambda element, area: (area[element.y][element.x - 1], element.y, element.x - 1),
    Direction.NORTH: lambda element, area: (area[element.y - 1][element.x], element.y - 1, element.x),
    Direction.SOUTH: lambda element, area: (area[element.y + 1][element.x], element.y + 1, element.x),
}


def get_element_by_direction(point: PipeElement, direction: Direction, area: list) -> tuple:
    """
    Return element from possible for element direction

    Return element, y, x of this new element

    Check INDEX OUT OF RANGE Error
    """
    return movements[direction](point, area)


assert get_element_by_direction(PipeElement(1, 2, Pipe.EAST_WEST), Direction.EAST, test_map_1) == ('7', 1, 3)
assert get_element_by_direction(PipeElement(3, 3, Pipe.NORTH_WEST), Direction.NORTH, test_map_1) == ('|', 2, 3)


def get_possible_movements(point: PipeElement) -> dict:
    """
        Return dictionary of moves
    """
    return pipe_paths_map[point.type]


def check_movement(pointer: PipeElement, area: list):
    """
    We have to check if element meet at movement is legal to move
    """
    moves = get_possible_movements(pointer)

    for direction_move in moves.keys():
        meet_element = get_element_by_direction(pointer, direction_move, area)

        """check if it is a pipe element ?"""
        if Pipe.is_pipe_element(meet_element):
            """Check is it legal to move on this position"""


            """add point to parth and go on!"""

