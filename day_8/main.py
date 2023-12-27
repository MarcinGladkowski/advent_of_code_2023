import re
from enum import Enum

from shared.main import load_data


class InstructionType(str, Enum):
    LEFT = 'L'
    RIGHT = 'R'


test_data = {
    'AAA': ['BBB', 'CCC'],
    'BBB': ['DDD', 'EEE'],
    'CCC': ['ZZZ', 'GGG'],
    'DDD': ['DDD', 'DDD'],
    'EEE': ['EEE', 'EEE'],
    'GGG': ['GGG', 'GGG'],
    'ZZZ': ['ZZZ', 'ZZZ']
}


def parse_data(data: list):
    """Prepare data loaded from file"""
    points = {}
    instructions = ''
    for i, line in enumerate(data):
        if i == 0:
            instructions = line
            continue

        if line == '':
            continue

        point_key, values = line.split('=')
        points[point_key.strip()] = re.sub("\s|(\()|(\))", "", values).split(',')

    return instructions, points


class Node:
    def __init__(self, id: int, start_point: str, current_point: str, iterator: int, has_finished: bool):
        self.id = id
        self.start_point = start_point
        self.current_point = current_point
        self.iterator = iterator
        self.has_finished = has_finished

    def is_end(self) -> bool:
        return self.has_finished

    def next(self, found_point: str):
        self.current_point = found_point
        self.has_finished = self.current_point.endswith('Z')
        self.iterator += 1

    def reset(self):
        self.has_finished = False


class NetworkRunner:
    def __init__(self, network: dict) -> None:
        self.network = network

    def get_point(self, code: str, instruction_type: InstructionType) -> str:

        point = self.get_point_name_by_code(code)

        return self.get_side_point_name(point, instruction_type)

    def get_point_name_by_code(self, code: str) -> list:
        return self.network[code]

    def reach_end_point(self, instructions: str, key: str = 'AAA', steps: int = 0) -> int:

        for i, instruction in enumerate(instructions):
            steps += 1
            point = self.get_point(key, InstructionType(instruction))

            if point == 'ZZZ':
                return steps

            key = point

            if i == len(instructions) - 1:
                return self.reach_end_point(instructions, key, steps)

    def reach_points_based_on_naming_strategy(self, instructions: str, key: callable = lambda x: x.endswith('A'), steps: int = 0, end_point: callable = lambda x: x.endswith('Z')):
        """
            key: starting point

            callback function which takes start and end points
        """

        for i, instruction in enumerate(instructions):
            steps += 1
            point = self.get_point(key, InstructionType(instruction))

            if end_point(point):
                return steps

            key = point

            if i == len(instructions) - 1:
                return self.reach_end_point(instructions, key, steps)


    def get_side_point_name(self, point: list, instruction: InstructionType) -> str:
        if instruction == InstructionType.LEFT:
            return point[0]

        if instruction == instruction.RIGHT:
            return point[1]

    def get_start_points(self):
        return list(filter(lambda x: x.endswith('A'), self.network.keys()))


networkRunner = NetworkRunner(test_data)

assert ['BBB', 'CCC'] == networkRunner.get_point_name_by_code('AAA')
assert 'CCC' == networkRunner.get_point('AAA', InstructionType.RIGHT)
assert 2 == networkRunner.reach_end_point('RL')

network_with_repeat = {
    'AAA': ['BBB', 'BBB'],
    'BBB': ['AAA', 'ZZZ'],
    'ZZZ': ['ZZZ', 'ZZZ'],
}

assert 6 == NetworkRunner(network_with_repeat).reach_end_point('LLR')


instructions, points = parse_data(load_data('input.txt'))

part_one = NetworkRunner(points)
assert 17621 == part_one.reach_end_point(instructions)


"""Part II"""
