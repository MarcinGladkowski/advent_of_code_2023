from dataclasses import dataclass
from abc import abstractmethod, ABC
from enum import Enum
from typing import Self


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
                case '|':
                    point = VerticalSplitter(y, x, element)

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

    def __str__(self):
        return f"Point {self.sign} - x:{self.x} - y:{self.y}"


class Dot(Point):
    def execute(self, direction: Direction) -> [Direction]:
        """
        Pass the same direction -> continue moving
        """
        return [
            direction
        ]


class VerticalSplitter(Point):
    """
       Sign: |
       Return two new directions: UP and DOWN
    """

    def execute(self, direction: Direction) -> [Direction]:
        return [
            Direction.UP,
            Direction.DOWN
        ]


class MapWalker:
    """
        List visited points in separate list/set (only unique values)
        - requires implement __hash__ method to point classes
    """

    def __init__(self, points_map: list, initial: Point, initial_move: Direction = Direction.RIGHT):
        self._points_map = points_map
        self._cursor = initial
        self._move = initial_move
        self._visited = set()
        self._visited.add(self._cursor)

    def next(self) -> Self | list:
        """
            Store visited Points
            - only unique Set
        """
        next_move = self._cursor.execute(self._move)

        if len(next_move) == 1:
            self._move = next_move[0]
            next_point = self.get_next_point(self._move)

            if next_point is None:
                return MapWalker

            self._cursor = next_point

            self._visited.add(self._cursor)
            return self.next()  # recursion

        mapped = [
            MapWalker(self._points_map, self.get_next_point(next_move))
            for point in next_move if self.get_next_point(point) is not None
        ]

        """ if returned more than one direction we need to start new two walkers"""
        return [
            MapWalker(self._points_map, self.get_next_point(next_move))
            for point in next_move if self.get_next_point(point) is not None
        ]

    def get_next_point(self, direction: Direction) -> Point | None:
        """
           Move on map by direction

           If key Error that's mean its jump over the edge

           While wall stop executing
        """
        map = self._points_map

        try:
            match direction:
                case Direction.RIGHT:

                    if x := self._cursor.x + 1 > len(self._points_map):
                        return None

                    return map[self._cursor.y][self._cursor.x + 1]
                case Direction.LEFT:

                    if x := self._cursor.x - 1 < 0:
                        return None

                    return map[self._cursor.y][x]
                case Direction.UP:

                    if y := self._cursor.y - 1 < 0:
                        return None

                    return map[y][self._cursor.x]
                case Direction.DOWN:

                    if y := self._cursor.y + 1 > len(self._points_map):
                        return None

                    return map[y][self._cursor.x]
        except IndexError:
            print(f"Out of map for coords move {direction} and coords {self._cursor}")
            return None
