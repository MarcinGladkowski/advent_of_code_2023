from typing import Generator


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
    elements = instructions.split(',')
    return sum([get_result(x) for x in elements])


def process_single_instruction(instruction: str, boxes: dict) -> dict:
    statement = instruction[2:3]  # =/-
    box_number = get_result(instruction[:2])
    value = instruction.replace(statement, ' ')

    """Create key if not exists"""
    if boxes.get(box_number) is None:
        boxes[box_number] = []

    match statement:
        case '=':
            return equal_strategy(value, boxes, box_number)
        case '-':
            return dash_strategy(value, boxes, box_number)

    return boxes


def equal_strategy(label: str, boxes: dict, box_number: int) -> dict:
    """
        strategy for: =
    """
    boxes[box_number].append(label)

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
