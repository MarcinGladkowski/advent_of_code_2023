import re
from enum import Enum

from shared.main import load_data


class InstructionType(str, Enum):
    LEFT = 'L'
    RIGHT = 'R'


network = {
    'AAA': ['BBB', 'CCC'],
    'BBB': ['DDD', 'EEE'],
    'CCC': ['ZZZ', 'GGG'],
    'DDD': ['DDD', 'DDD'],
    'EEE': ['EEE', 'EEE'],
    'GGG': ['GGG', 'GGG'],
    'ZZZ': ['ZZZ', 'ZZZ']
}


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

    def reach_end_point(
            self,
            instructions: str,
            key: str = 'AAA',
            steps: int = 0,
            end_point: callable = lambda x: x == 'ZZZ',
    ) -> int:

        for i, instruction in enumerate(instructions):
            steps += 1
            point = self.get_point(key, InstructionType(instruction))

            if end_point(point):
                return steps

            key = point

            if i == len(instructions) - 1:
                return self.reach_end_point(instructions, key, steps, end_point)

    def get_side_point_name(self, point: list, instruction: InstructionType) -> str:
        if instruction == InstructionType.LEFT:
            return point[0]

        if instruction == instruction.RIGHT:
            return point[1]

    def simultaneously_start(self, instructions: str):
        """
        Execute in loop for elements ending with A
        Ending on elements ending with Z
        """
        start_points = list(filter(lambda x: x.endswith('A'), self.network.keys()))

        nodes = []
        for i, start_point in enumerate(start_points):
            nodes.append(Node(i, start_point, start_point, 0, False))

        # result = 0
        # for instruction in instructions:
        #     nodes = self.reach_points_on_single_instruction(nodes, InstructionType(instruction))
        #
        #     if self.all_nodes_finished(nodes):
        #         return self.all_nodes_count(nodes)
        #
        #     result += 1
        #     self.reset_nodes(nodes)
        #
        # return result

        result = self.recursion_nodes(nodes, instructions)

        return result

    def recursion_nodes(self, nodes, instructions, result=0):

        for instruction in instructions:
            nodes = self.reach_points_on_single_instruction(nodes, InstructionType(instruction))

            if self.all_nodes_finished(nodes):
                return nodes[0].iterator

            result += 1
            self.reset_nodes(nodes)

        return self.recursion_nodes(nodes, instructions, result)

    def reach_points_on_single_instruction(self, nodes, instruction: InstructionType):

        for node in nodes:
            found_point = self.get_point(node.current_point, InstructionType(instruction))
            node.next(found_point)

        return nodes

    def all_nodes_finished(self, nodes: list) -> bool:
        return len(list(filter(lambda node: node.has_finished, nodes))) == len(nodes)

    def all_nodes_count(self, nodes) -> int:
        return sum(list(map(lambda node: node.iterator, nodes)))

    def reset_nodes(self, nodes):
        for node in nodes:
            node.reset()


networkRunner = NetworkRunner(network)

assert ['BBB', 'CCC'] == networkRunner.get_point_name_by_code('AAA')
assert 'CCC' == networkRunner.get_point('AAA', InstructionType.RIGHT)
assert 2 == networkRunner.reach_end_point('RL')

network_with_repeat = {
    'AAA': ['BBB', 'BBB'],
    'BBB': ['AAA', 'ZZZ'],
    'ZZZ': ['ZZZ', 'ZZZ'],
}

assert 6 == NetworkRunner(network_with_repeat).reach_end_point('LLR')


def parse_data(data: list):
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


instructions, points = parse_data(load_data('input.txt'))

part_one = NetworkRunner(points)
assert 17621 == part_one.reach_end_point(instructions)

instructions, points = parse_data(load_data('test_input.txt'))

part_two = NetworkRunner(points)
assert 6 == part_two.simultaneously_start(instructions)

"""
104674 too low
124662 (20777*6)
"""
# instructions, points = parse_data(load_data('input.txt'))
#
# part_two = NetworkRunner(points)
# print(part_two.simultaneously_start(instructions))
