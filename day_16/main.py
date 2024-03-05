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
                    point = Dot(x, y, element)

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
    """Abstract class for traversing"""
    x: int
    y: int
    sign: str

    @abstractmethod
    def execute(self, direction: Direction) -> [Direction]:
        pass


class Dot(Point):
    def execute(self, direction: Direction):
        """
        Pass the same direction -> continue moving
        """
        return [
            Direction
        ]


class MapWalker:
    def __init__(self, map: list, initial: Point):
        self._map = map

    def next(self):
        pass
