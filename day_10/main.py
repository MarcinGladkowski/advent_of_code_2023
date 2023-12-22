from enum import Enum


# class Directions(Enum):
#     NORTH = 'north'


class Pipe(Enum):
    NORTH_SOUTH = '|'
    EAST_WEST = '-'
    NORTH_EAST = 'L'
    NORTH_WEST = 'J'
    SOUTH_WEST = '7'
    SOUTH_EAST = 'F'


class Direction(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    WEST = 'west'
    EAST = 'east'


pipe_paths_map = {
    Pipe.NORTH_SOUTH: {
        'north': [Pipe.SOUTH_EAST, Pipe.SOUTH_WEST, Pipe.NORTH_SOUTH],
        'south': [Pipe.NORTH_EAST, Pipe.NORTH_WEST, Pipe.NORTH_SOUTH]
    },
    Pipe.EAST_WEST: {
        'west': [Pipe.EAST_WEST, Pipe.SOUTH_EAST, Pipe.NORTH_EAST],
        'east': [Pipe.EAST_WEST, Pipe.NORTH_WEST, Pipe.SOUTH_WEST]
    },
    Pipe.NORTH_EAST: {
        'north': [Pipe.NORTH_SOUTH, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST],
        'east': [Pipe.EAST_WEST, Pipe.NORTH_WEST, Pipe.SOUTH_WEST]
    },
    Pipe.NORTH_WEST: {
        'north': [Pipe.NORTH_SOUTH, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST],
        'west': [Pipe.EAST_WEST, Pipe.NORTH_EAST, Pipe.SOUTH_EAST]
    },
    Pipe.SOUTH_WEST: {
        'south': [Pipe.NORTH_SOUTH, Pipe.NORTH_EAST, Pipe.NORTH_WEST],
        'west': [Pipe.SOUTH_WEST, Pipe.SOUTH_EAST, Pipe.NORTH_EAST],
    },
    Pipe.SOUTH_EAST: {
        'south': [Pipe.NORTH_SOUTH, Pipe.NORTH_EAST, Pipe.NORTH_WEST],
        'east': [Pipe.EAST_WEST, Pipe.SOUTH_WEST, Pipe.NORTH_WEST]
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
    pass


'''
Check neighbors to choose correct movement or break path.

Test of element y, x => (1, 2) => '-'
'''
movements = {
    Direction.EAST: lambda element, area: area[element.y][element.x + 1],
    Direction.WEST: lambda element, area: area[element.y][element.x - 1],
    Direction.NORTH: lambda element, area: area[element.y - 1][element.x],
    Direction.SOUTH: lambda element, area: area[element.y + 1][element.x],
}


def get_element_by_direction(point: PipeElement, direction: Direction, area: list):
    return movements[direction](point, area)


assert get_element_by_direction(PipeElement(1, 3, Pipe.EAST_WEST), Direction.EAST, test_map_1) == '7'

def get_possible_movements(point: PipeElement) -> dict:
    return pipe_paths_map[point.type]

def check_movement(pointer: PipeElement, area: list):
    moves = get_possible_movements(pointer)
