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


pipe_paths_map = {
    Pipe.NORTH_SOUTH: {
        'north': [Pipe.SOUTH_EAST, Pipe.SOUTH_WEST, Pipe.NORTH_SOUTH],
        'south': [Pipe.NORTH_EAST, Pipe.NORTH_WEST, Pipe.NORTH_SOUTH]
    },
    Pipe.EAST_WEST: {
        'west': [Pipe.EAST_WEST, Pipe.SOUTH_EAST, Pipe.NORTH_EAST],
        'east': [Pipe.EAST_WEST, Pipe.NORTH_WEST, Pipe.SOUTH_WEST]
    }
}
