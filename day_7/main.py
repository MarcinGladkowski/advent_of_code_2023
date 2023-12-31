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
        self.jocker_usage = None
        self.bid = bid

    def get_with_jocker_type(self):

        unique = set(filter(lambda x: x != 'J', list(self.set)))

        if len(set(unique)) == 0:
            return self.get_type()

        highest_solution = Type.HIGH_CARD
        for unique_sign in unique:
            candidate = self.get_type(
                self.set.replace('J', unique_sign)
            )

            if candidate.value > highest_solution.value:
                highest_solution = candidate
                self.jocker_usage = self.set.replace('J', unique_sign)


        return self.get_type() if highest_solution is None else highest_solution

    def get_type(self, from_set: str = None) -> Type:

        card_set = self.set if from_set is None else from_set

        """
         Where is FULL type ?
        :return:
        """
        if self._occurences_of_same_cards_count(card_set, 5):
            return Type.FIVE

        if self._occurences_of_same_cards_count(card_set, 4):
            return Type.FOUR

        if self._occurences_of_same_cards_count(card_set, 3, 1) \
                and self._occurences_of_same_cards_count(card_set, 2, 1):
            return Type.FULL

        if self._occurences_of_same_cards_count(card_set, 3):
            return Type.THREE

        if self._occurences_of_same_cards_count(card_set, 2, 2):
            return Type.TWO_PAIR

        if self._occurences_of_same_cards_count(card_set, 2):
            return Type.ONE_PAIR

        return Type.HIGH_CARD

    def _occurences_of_same_cards_count(self, set: str, occurence_of_combination: int, count: int = 1):
        return operator.countOf(list(Counter(set).values()), occurence_of_combination) == count


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
assert Type.FOUR == CardSet('22223', 765).get_type()
assert Type.FULL == CardSet('22333', 765).get_type()


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


cards_with_joker = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class JockerCardSetsComparator:
    @staticmethod
    def compare(set_a: CardSet, set_b: CardSet):
        """
            Is the set_a > than set_b
            The same set - compare cards one by one
            Not the same - compare Type
        """
        if set_a.get_with_jocker_type() == set_b.get_with_jocker_type():
            """Compare cards"""
            for i in range(5):
                if set_a.set[i] == set_b.set[i]:
                    continue
                return cards_with_joker.index(set_a.set[i]) > cards_with_joker.index(set_b.set[i])

        return set_a.get_with_jocker_type().value > set_b.get_with_jocker_type().value


assert CardSetsComparator.compare(CardSet('TTTTT', 765), CardSet('32T3K', 765))
assert CardSetsComparator.compare(CardSet('KK677', 765), CardSet('KTJJT', 765))
assert CardSetsComparator.compare(CardSet('T55J5', 765), CardSet('KK677', 765))


def parse_to_card_desk(data: list) -> list:
    desk = []
    for line in data:
        card_set, bid = line.split(' ')
        desk.append(CardSet(card_set, int(bid)))
    return desk


def bubble_sort(comparator, array):
    n = len(array)

    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if comparator.compare(array[j], array[j + 1]):
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break

    return array


sorted_test_cards_desk = bubble_sort(CardSetsComparator, test_cards_desk)

expected_order = [
    CardSet('QQQJA', 483),
    CardSet('T55J5', 684),
    CardSet('KK677', 28),
    CardSet('KTJJT', 220),
    CardSet('32T3K', 765),
]


def calculate_result(comparator, desk: list) -> int:
    sum = 0
    sort_desk = bubble_sort(comparator, desk)

    for i, card in enumerate(sort_desk):
        sum += card.bid * (i + 1)
    return sum


assert 6440 == calculate_result(CardSetsComparator, parse_to_card_desk(test_data))
assert 5905 == calculate_result(JockerCardSetsComparator, parse_to_card_desk(test_data))

data = load_data('input.txt')
assert len(parse_to_card_desk(data)) == 1000

assert 253313241 == calculate_result(parse_to_card_desk(data))

assert Type.FOUR == CardSet('QJJQ2', 100).get_with_jocker_type()
assert JockerCardSetsComparator.compare(CardSet('QQQJA', 765), CardSet('T55J5', 765))
assert JockerCardSetsComparator.compare(CardSet('QQQQ2', 765), CardSet('JKKK2', 765))

assert 253362743 == calculate_result(JockerCardSetsComparator, parse_to_card_desk(data))
