from shared.main import load_data
import re

test_data = load_data('input_test.txt')


def card_number_from_title(title: str) -> int:
    match = re.search('\d{1,}', title)

    if match:
        return int(match.group(0))


def transform_list(numbers: str) -> list:
    return list(
        map(lambda x: int(x),
            filter(lambda x: x.isnumeric(), numbers.split(' ')))
    )


class Card:

    def __init__(self, id: int, win_numbers: list, numbers: list):
        self.int = id
        self.win_numbers = win_numbers
        self.numbers = numbers

    def get_overlapped(self):
        return set(self.win_numbers) & set(self.numbers)

    def calculate_points(self):
        """
        1,2,4,8 = 2**3
        :return:
        """
        power = len(list(self.get_overlapped())) - 1

        if power < 0:
            return 0

        return 2 ** power


def parse_cards(data: str) -> list:
    cards = []

    for card in data:
        win_numbers, numbers = card.split('|')

        title, win_numbers = win_numbers.split(':')

        card_round = Card(
            card_number_from_title(title),
            transform_list(win_numbers),
            transform_list(numbers)
        )

        cards.append(card_round)

    return cards


def calculate_sum(parsed: list):
    result = 0
    for lottery_card in parsed:
        result += lottery_card.calculate_points()

    return result


assert calculate_sum(parse_cards(test_data)) == 13

data = load_data('input.txt')

assert calculate_sum(parse_cards(data)) == 25231 # day one part_1
