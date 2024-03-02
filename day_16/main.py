from dataclasses import dataclass


def normalize_data(data: list):
    normalized = []
    for y, row in enumerate(data):
        row = []
        for x, element in enumerate(data[y]):
            row.append(Point(x, y))

        normalized.append(row)

    return normalized


@dataclass
class Point:
    x: int
    y: int
