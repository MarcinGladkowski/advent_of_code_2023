import unittest

from main import equal_strategy, dash_strategy, calculate_hash, get_result, calculate_from_instruction, \
    process_single_instruction
from shared.main import load_data

test_input = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

generator = calculate_hash('HASH')

assert 200 == next(generator)
assert 153 == next(generator)
assert 172 == next(generator)
assert 52 == next(generator)

assert 52 == get_result('HASH')

"""test input"""
assert 30 == get_result('rn=1')

assert 1320 == calculate_from_instruction(test_input)

"""part 1"""
assert 507291 == calculate_from_instruction(load_data('input_data.txt')[0])

"""part 2"""
assert 3 == get_result('pc')  # box number


class PartTwo(unittest.TestCase):
    def test_add_single_element(self):
        assert ['rn 1'] == process_single_instruction('rn=1', {})[0]

    def test_add_two_elements_to_both_boxes(self):
        box = {}
        box = process_single_instruction('rn=1', box)
        box = process_single_instruction('qp=3', box)

        assert ['rn 1'] == box[0]
        assert ['qp 3'] == box[1]

    def test_add_second_element_to_same_box(self):
        box = {}
        box = process_single_instruction('rn=1', box)
        box = process_single_instruction('cm=2', box)

        assert ['rn 1', 'cm 2'] == box[0]

    def test_equal_add_element_to_box_zero(self):
        box = {
            0: ['rn 1'],
        }

        assert ['rn 1', 'cm 2'] == equal_strategy('cm 2', box, 0)[0]

    def test_dash_removing_single_element(self):
        box = {
            0: ['rn 1', 'cm 2'],
        }

        assert ['rn 1'] == dash_strategy('cm-', box, 0)[0]

    def test_equal_strategy_replacing_existing_label(self):
        box = {
            3: ['ot 7', 'ab 5', 'pc 6'],
        }

        assert ['ot 9', 'ab 5', 'pc 6'] == equal_strategy('ot 9', box, 3)[3]
