from enum import Enum


class InstructionType(str, Enum):
    LEFT = 'L'
    RIGHT = 'R'


instructions = 'RL'

'''
AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''

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

    def reach_end_point(self, instructions: str, key: str = 'AAA') -> int:
        steps = 0

        for instruction in instructions:
            steps += 1
            point = self.get_point(key, InstructionType(instruction))

            if point == 'ZZZ':
                return steps

            key = point


networkRunner = NetworkRunner(network)

assert ['BBB', 'CCC'] == networkRunner.get_point_name_by_code('AAA')
assert 'CCC' == networkRunner.get_point('AAA', InstructionType.RIGHT)
assert 2 == networkRunner.reach_end_point(instructions)
