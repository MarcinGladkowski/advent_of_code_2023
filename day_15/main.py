import re
from pprint import pprint
from typing import Generator

DEBUG = False


def calculate_hash(chars: str, value: int = 0, index: int = 0) -> Generator:
    while index < len(chars):
        result = ((ord(chars[index]) + value) * 17) % 256
        yield result
        index += 1
        value = result


def get_result(chars: str):
    generator = calculate_hash(chars)
    result = 0
    try:
        while True:
            result = next(generator)
    except StopIteration:
        return result


def calculate_from_instruction(instructions: str) -> int:
    """Part 1 solution"""
    elements = instructions.split(',')
    return sum([get_result(x) for x in elements])


def calculate_box_row(box_row: list, index: 0) -> int:

    box_sum = 0
    for i, x in enumerate(box_row):
        box_sum += int(i + 1) * int(x[-1]) * (index + 1)

    print(f"box_index: {index} - box - {box_row} - sum: {box_sum}")

    return box_sum


def process_instruction_to_boxes(instructions: str) -> dict:
    instructions = instructions.split(',')
    boxes = {}
    for instruction in instructions:
        boxes = process_single_instruction(instruction, boxes)

    return boxes


def calculate_boxes(boxes: dict) -> int:
    sum = 0
    for i, box in boxes.items():
        sum += calculate_box_row(box, i)

    return sum


def get_label(instruction: str) -> str:
    return re.sub(r'[-|=\d+]', '', instruction)


def process_single_instruction(instruction: str, boxes: dict) -> dict:
    statement = None

    if re.search('=', instruction) is not None:
        statement = '='
    if re.search('-', instruction) is not None:
        statement = '-'

    label = get_label(instruction)

    box_number = get_result(label)
    value = instruction.replace(statement, ' ')

    """Create key if not exists"""
    if boxes.get(box_number) is None:
        boxes[box_number] = []

    if DEBUG:
        boxes[box_number].append(instruction)
        return boxes

    match statement:
        case '=':
            boxes = equal_strategy(value, boxes, box_number)
        case '-':
            boxes = dash_strategy(value, boxes, box_number)

    return boxes


def equal_strategy(label: str, boxes: dict, box_number: int) -> dict:
    """
        strategy for: =
    """
    label_name = label[:2]

    in_list = list(filter(
        lambda x: x.startswith(label_name) is True,
        boxes[box_number])
    )

    if len(in_list) == 0:
        boxes[box_number].append(label)
        return boxes

    elements = boxes[box_number]
    for i, element in enumerate(elements):
        if element.startswith(label_name):
            elements[i] = label
            break

    boxes[box_number] = elements

    return boxes


def dash_strategy(label: str, boxes: dict, box_number: int) -> dict:
    """
       param: label e.g. 'rm 2'
       strategy for: -
    """
    label_name = label[:2]
    filter_not_matching = list(filter(
        lambda x: x.startswith(label_name) is False,
        boxes[box_number])
    )

    boxes[box_number] = filter_not_matching

    return boxes
