import re
import unittest
from pprint import pprint

from main import equal_strategy, dash_strategy, calculate_hash, get_result, calculate_from_instruction, \
    process_single_instruction, process_instruction_to_boxes, calculate_box_row, calculate_boxes, get_label
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

    def test_process_single_instruction_from_custom_instruction_length(self):
        assert ['slxgsf 7'] == process_single_instruction('slxgsf=7', {})[135]

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


    def test_dash_strategy_to_remove_first_element(self):

        box = {
            3: ['pc 4', 'ot 9', 'ab 5']
        }

        assert ['ot 9', 'ab 5'] == dash_strategy('pc-', box, 3)[3]

    def test_equal_strategy_replacing_existing_label(self):
        box = {
            3: ['ot 9', 'ab 5', 'pc 6'],
        }

        assert ['ot 7', 'ab 5', 'pc 6'] == equal_strategy('ot 7', box, 3)[3]

    def test_equal_test_input_instructions(self):

        boxes = process_instruction_to_boxes('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7')

        assert ['rn 1', 'cm 2'] == boxes[0]
        assert ['ot 7', 'ab 5', 'pc 6'] == boxes[3]

    def test_calculate_single_box_row(self):
        assert 140 == calculate_box_row(['ot 7', 'ab 5', 'pc 6'], 3)

    def test_label_processing(self):
        assert 'rn' == get_label('rn=1')
        assert 'cm' == get_label('cm-')
        assert 'pc' == get_label('pc-')

    def test_generate_boxes_for_test_data(self):
        boxes = process_instruction_to_boxes('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7')

        assert ['rn 1', 'cm 2'] == boxes[0]
        assert ['ot 7', 'ab 5', 'pc 6'] == boxes[3]

    def test_calculates_test_input(self):
        assert 145 == calculate_boxes(process_instruction_to_boxes('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'))

    def test_calculate_part_two(self):
        # 59717 too low, 293485 - to low, 603482 - to high
        boxes = process_instruction_to_boxes(load_data('input_data.txt')[0])
        #pprint(boxes)
        result = calculate_boxes(boxes)
        print(result)

        assert True