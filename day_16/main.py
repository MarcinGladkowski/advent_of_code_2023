from dataclasses import dataclass
from abc import abstractmethod, ABC
from enum import Enum


def normalize_data(data: list):
    normalized = []
    for y, row in enumerate(data):
        row = []
        for x, element in enumerate(data[y]):
            # strategy for creating object ?
            point = None

            match element:
                case '.':
                    point = Dot(y, x, element)

            row.append(point)

        normalized.append(row)

    return normalized


class Direction(Enum):
    """All available directions"""
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'


@dataclass
class Point(ABC):
    """
        Abstract class for traversing
        - keep order of arguments
    """
    y: int
    x: int
    sign: str

    @abstractmethod
    def execute(self, direction: Direction) -> [Direction]:
        pass

    def __hash__(self):
        return hash(str(self.y) + '-' + str(self.x))


class Dot(Point):
    def execute(self, direction: Direction):
        """
        Pass the same direction -> continue moving
        """
        return direction


class MapWalker:
    """
        List visited points in separate list/set (only unique values)
        - requires implement __hash__ method to point classes
    """
    def __init__(self, points_map: list, initial: Point, initial_move: Direction = Direction.RIGHT):
        self._points_map = points_map
        self._cursor = initial
        self._move = initial_move
        # store visited elements

    def next(self) -> None:
        """
            Store visited Points
            - only unique Set
        """
        direction = self._cursor.execute(self._move)  # get new element by returned direction

        # getting element by direction
        self._cursor = self.get_next_point(direction)

    def get_next_point(self, direction: Direction) -> Point:
        """
           Move on map by direction

           If key Error that's mean its jump over the edge
        """
        match direction:
            case Direction.RIGHT:
                return self._points_map[self._cursor.y][self._cursor.x + 1]
            case Direction.LEFT:
                return self._points_map[self._cursor.y][self._cursor.x - 1]
            case Direction.UP:
                return self._points_map[self._cursor.y + 1][self._cursor.x]
            case Direction.DOWN:
                return self._points_map[self._cursor.y - 1][self._cursor.x]

