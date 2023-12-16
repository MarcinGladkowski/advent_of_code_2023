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

        count_cards_occurences = list(Counter(self.set).values())

        if operator.countOf(count_cards_occurences, 5) == 1:
            return Type.FIVE

        if operator.countOf(count_cards_occurences, 4) == 1:
            return Type.FOUR

        if operator.countOf(count_cards_occurences, 2) == 2:
            return Type.TWO_PAIR

        if operator.countOf(count_cards_occurences, 3) == 1:
            return Type.THREE

        if operator.countOf(count_cards_occurences, 2) == 1:
            return Type.ONE_PAIR

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