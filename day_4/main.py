from shared.main import load_data
import re

test_data = load_data('input_test.txt')
data = load_data('input.txt')


def flatten(test_list):
    if isinstance(test_list, list):
        if len(test_list) == 0:
            return []
        first, rest = test_list[0], test_list[1:]
        return flatten(first) + flatten(rest)
    else:
        return [test_list]


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
        self.id = id
        self.win_numbers = win_numbers
        self.numbers = numbers

    def get_overlapped(self):
        return set(self.win_numbers) & set(self.numbers)

    def count_win(self):
        return len(self.get_overlapped())

    def is_win(self):
        return self.count_win() > 0

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

assert calculate_sum(parse_cards(data)) == 25231  # day one part_1

test_cards = parse_cards(test_data)


def recursive_win_counter(data: list, card: Card, node_elements: list):

    print(f"Recursive calculating {card.id}")

    if card.is_win() is False:
        return node_elements

    # result = []
    #
    # for win_copy_id in range(0, card.count_win() + 1):
    #     result.append(
    #         recursive_win_counter(data, data[card.id + win_copy_id], node_elements)
    #     )
    #
    # return result
    print(card.count_win())

    return list(
        recursive_win_counter(data, data[card.id + win_copy_id], node_elements)
        for win_copy_id in range(1, card.count_win() + 1)
    )


def calculate_for_card(data: list, card: Card):
    return recursive_win_counter(data, card, [card])


#assert 7 == len(flatten(calculate_for_card(test_cards, test_cards[1])))


def calculate(data: list):
    total = 0
    for card in data:
        print(f"Processing {card.id}")
        total += len(flatten(calculate_for_card(data, card)))
    return total


# assert 30 == calculate(test_cards)

print(calculate(parse_cards(data)))
