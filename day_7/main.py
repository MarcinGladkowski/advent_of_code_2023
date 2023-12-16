import operator
from enum import Enum
from collections import Counter


cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


class Type(Enum):
    FIVE = 5
    FOUR = 4
    FULL = 3
    THREE = 2
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

'''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
cards_desk = [
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