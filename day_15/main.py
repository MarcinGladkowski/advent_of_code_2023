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
    statement = None
    if '=' in instruction:
        statement = '='

    if '-' in instruction:
        statement = '-'

    box_number = get_result(instruction[:2]) + 1

    value = instruction.replace(statement, '')

    boxes[box_number] = [value]

    return boxes
