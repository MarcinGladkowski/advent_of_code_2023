import operator
from enum import Enum
from collections import Counter

from shared.main import load_data

test_data = load_data('test_input.txt')

cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


class Type(Enum):
    FIVE = 6
    FOUR = 5
    FULL = 4
    THREE = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0  # no combinations


class CardSet:
    def __init__(self, set: str, bid: int):
        self.set = set
        self.bid = bid

    def get_type(self) -> Type:

        if self._occurences_of_same_cards_count(5):
            return Type.FIVE

        if self._occurences_of_same_cards_count(4):
            return Type.FOUR

        if self._occurences_of_same_cards_count(3):
            return Type.THREE

        if self._occurences_of_same_cards_count(2, 2):
            return Type.TWO_PAIR

        if self._occurences_of_same_cards_count(2):
            return Type.ONE_PAIR

        return Type.HIGH_CARD

    def _occurences_of_same_cards_count(self, occurence_of_combination: int, count: int = 1):
        return operator.countOf(list(Counter(self.set).values()), occurence_of_combination) == count


test_cards_desk = [
    CardSet('32T3K', 765),
    CardSet('T55J5', 684),
    CardSet('KK677', 28),
    CardSet('KTJJT', 220),
    CardSet('QQQJA', 483),
]

assert Type.ONE_PAIR == CardSet('32T3K', 765).get_type()
assert Type.THREE == CardSet('T55J5', 765).get_type()
assert Type.TWO_PAIR == CardSet('KK677', 765).get_type()
assert Type.FOUR == CardSet('AA7AA', 765).get_type()
assert Type.FIVE == CardSet('TTTTT', 765).get_type()
assert Type.HIGH_CARD == CardSet('23456', 765).get_type()


class CardSetsComparator:
    @staticmethod
    def compare(set_a: CardSet, set_b: CardSet):
        """
            Is the set_a > than set_b
            The same set - compare cards one by one
            Not the same - compare Type
        """
        if set_a.get_type() == set_b.get_type():
            """Compare cards"""
            for i in range(5):
                if set_a.set[i] == set_b.set[i]:
                    continue
                return cards.index(set_a.set[i]) > cards.index(set_b.set[i])

        return set_a.get_type().value > set_b.get_type().value


assert CardSetsComparator.compare(CardSet('TTTTT', 765), CardSet('32T3K', 765))
assert CardSetsComparator.compare(CardSet('KK677', 765), CardSet('KTJJT', 765))
assert CardSetsComparator.compare(CardSet('T55J5', 765), CardSet('KK677', 765))


def parse_to_card_desk(data: list) -> list:
    desk = []
    for line in data:
        card_set, bid = line.split(' ')
        desk.append(CardSet(card_set, int(bid)))
    return desk


def bubble_sort(array):
    n = len(array)

    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if CardSetsComparator.compare(array[j], array[j + 1]):
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break

    return array


sorted_test_cards_desk = bubble_sort(test_cards_desk)

expected_order = [
    CardSet('QQQJA', 483),
    CardSet('T55J5', 684),
    CardSet('KK677', 28),
    CardSet('KTJJT', 220),
    CardSet('32T3K', 765),
]


def calculate_result(desk: list) -> int:
    sum = 0

    sort_desk = bubble_sort(desk)

    for i, card in enumerate(sort_desk):
        sum += card.bid * (i + 1)

    return sum


assert 6440 == calculate_result(parse_to_card_desk(test_data))


data = load_data('input.txt')
"""
Result to high: 253514144
"""
#print(len(parse_to_card_desk(data)) == 1000)


print(
    calculate_result(parse_to_card_desk(data))
)