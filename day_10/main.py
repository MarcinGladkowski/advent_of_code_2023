from enum import Enum


class Pipe(Enum):
    NORTH_SOUTH = '|'
    EAST_WEST = '-'
    NORTH_EAST = 'L'
    NORTH_WEST = 'J'
    SOUTH_WEST = '7'
    SOUTH_EAST = 'F'
    STARTING_POINT = 'S'
    GROUND = '.'

    def is_starting_point(self):
        return self.value == Pipe.STARTING_POINT.value

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

    def __eq__(self, other):
        return (self.y, self.x, self.type.value) == (other.y, other.x, other.type.value)

    def __str__(self):
        return f"Position {self.y} - {self.x} | {self.type.value}"


assert PipeElement(1, 1, Pipe.NORTH_WEST) == PipeElement(1, 1, Pipe.NORTH_WEST)


class Path:

    def __init__(self, pipe_elements: list = None):
        self.pipe_elements = [] if pipe_elements is None else pipe_elements

    def add(self, pipe_element: PipeElement):
        self.pipe_elements.append(pipe_element)

    def next(self, pipe_element: PipeElement) -> None:
        self.pipe_elements.append(pipe_element)

    def pointer(self):
        """
        Last element in path is a pointer/position
        """
        return self.pipe_elements[-1]

    def has_previous(self) -> bool:
        return len(self.pipe_elements) > 1

    def previous(self):
        if len(self.pipe_elements) == 1:
            return None

        return self.pipe_elements[-2]

    def has(self, pipe_element: PipeElement):
        for el in self.pipe_elements:
            if el == pipe_element:
                return True

        return False




'''
Check neighbors to choose correct movement or break path.

Test of element y, x => (1, 2) => '-'
'''
movements = {
    Direction.EAST: lambda element, area: (area[element.y][element.x + 1], element.y, element.x + 1),
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


def move(path: Path, area: list) -> Path:
    """
    We have to check if element meet at movement is legal to move and return new Point to Path if it's valid
    """
    pointer = path.pointer()
    previous = path.previous()

    moves = get_possible_movements(pointer)

    """
        There is a situation when two directions are possible to move
        One directions was used by previous position
    """
    for direction_move, direction_move_possibilities in moves.items():
        meet_element, meet_element_y, meet_element_x = get_element_by_direction(pointer, direction_move, area)

        next_possible_pipe_element = Pipe(meet_element)

        """Omit checking on start by remember to find ending of path loop"""
        if path.has_previous() and previous.type.is_starting_point():
            continue

        """Previous is in path and was parsed"""
        if path.has(PipeElement(meet_element_y, meet_element_x, next_possible_pipe_element)):
            continue

        if path.has_previous() and next_possible_pipe_element.is_starting_point():
            return path

        if next_possible_pipe_element in direction_move_possibilities:
            path.add(
                PipeElement(meet_element_y, meet_element_x, next_possible_pipe_element)
            )

            return move(path, area)


"""
    Do I need add start and finish point - simple parsing example data
    
    To count result of the path I need add starting point. In this example 7 + 1
"""
assert 7 == len(move(Path([PipeElement(1, 2, Pipe.EAST_WEST)]), test_map_1).pipe_elements)

test_map_2 = [
    ['7', '-', 'F', '7', '-'],
    ['.', 'F', 'J', '|', '7'],
    ['S', 'J', 'L', 'L', '7'],
    ['|', 'F', '-', '-', 'J'],
    ['L', 'J', '.', 'L', 'J']
]

"""
Start all move from points around starting point (S)
"""
correct_path_test_map_2 = move(Path([PipeElement(2, 1, Pipe.NORTH_WEST)]), test_map_2)

print(len(correct_path_test_map_2.pipe_elements))

from shared.main import load_data

data_part_1 = load_data('input.txt')

parsed_map = []
for index, row in enumerate(data_part_1):
    line_parsed = []
    for el in row:
        line_parsed.append(el)
    parsed_map.append(line_parsed)


print(parsed_map)