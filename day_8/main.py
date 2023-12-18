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


class NetworkRunner:
    def __init__(self, network: dict) -> None:
        self.network = network
        self.simultaneously_finished = 0

    def get_point(self, code: str, instruction_type: InstructionType) -> str:

        point = self.get_point_name_by_code(code)

        return self.get_side_point_name(point, instruction_type)

    def get_point_name_by_code(self, code: str) -> list:
        return self.network[code]

    def get_side_point_name(self, point: list, instruction: InstructionType) -> str:
        if instruction == InstructionType.LEFT:
            return point[0]

        if instruction == instruction.RIGHT:
            return point[1]

    def reach_end_point(self, instructions: str, key: str = 'AAA', steps: int = 0,
                        end_point: callable = lambda x: x == 'ZZZ') -> int:

        for i, instruction in enumerate(instructions):
            steps += 1
            point = self.get_point(key, InstructionType(instruction))

            if end_point(point):
                print(f"Finished at {point}")
                return steps

            key = point

            if i == len(instructions) - 1:
                return self.reach_end_point(instructions, key, steps, end_point)

    def simultaneously_start(self, instructions: str):
        """
        Execute in loop for elements ending with A
        Ending on elements ending with Z
        """
        starting_points = list(filter(lambda x: x.endswith('A'), self.network.keys()))
        result = 0

        print(starting_points)

        for start_point in starting_points:
            point_result = self.reach_end_point(instructions, start_point, 0, lambda x: x.endswith('Z'))
            print(point_result)
            result += point_result


        return result


networkRunner = NetworkRunner(network)

# assert ['BBB', 'CCC'] == networkRunner.get_point_name_by_code('AAA')
# assert 'CCC' == networkRunner.get_point('AAA', InstructionType.RIGHT)
# assert 2 == networkRunner.reach_end_point('RL')

network_with_repeat = {
    'AAA': ['BBB', 'BBB'],
    'BBB': ['AAA', 'ZZZ'],
    'ZZZ': ['ZZZ', 'ZZZ'],
}

# assert 6 == NetworkRunner(network_with_repeat).reach_end_point('LLR')


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

# part_one = NetworkRunner(points)
# assert 17621 == part_one.reach_end_point(instructions)

"""
104674 too low
124662 (20777*6)
"""
instructions, points = parse_data(load_data('input.txt'))

part_two = NetworkRunner(points)
print(part_two.simultaneously_start(instructions))