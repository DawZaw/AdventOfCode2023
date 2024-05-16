import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


from typing import Self


class Hand:
    cards: str
    bid: int
    hand_type: int
    card_values: list[int]

    def __init__(self, cards: str, bid: str) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.card_values = self.get_card_values()
        self.hand_type = self.get_hand_type()

    def count_cards(self) -> list[int]:
        return [self.cards.count(card) for card in set(self.cards)]

    def get_hand_type(self) -> int:
        """
        Five of a kind = 6
        Four of a kind = 5
        Full house = 4
        Three of a kind = 3
        Two pairs = 2
        One pair = 1
        High card = 0
        """
        card_count: list[int] = self.count_cards()
        if 5 in card_count:
            return 6
        if 4 in card_count:
            return 5
        if 3 in card_count:
            if 2 in card_count:
                return 4
            return 3
        if 2 in card_count:
            if card_count.count(2) == 2:
                return 2
            return 1
        return 0

    def get_card_values(self) -> list[int]:
        values: dict[str, int] = {
            "A": 12,
            "K": 11,
            "Q": 10,
            "J": 9,
            "T": 8,
            "9": 7,
            "8": 6,
            "7": 5,
            "6": 4,
            "5": 3,
            "4": 2,
            "3": 1,
            "2": 0,
        }
        return [values[card] for card in self.cards]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        else:
            return (self.hand_type, self.card_values) == (
                other.hand_type,
                other.card_values,
            )

    def __lt__(self, other: Self) -> bool:
        return (self.hand_type, self.card_values) < (other.hand_type, other.card_values)


with open(filepath, "r") as file:
    hands: list[Hand] = [Hand(*line.split(" ")) for line in file.readlines()]

    hands.sort()
    total: int = 0
    for i, hand in enumerate(hands):
        total += hand.bid * (i + 1)

    print(f"Part 1: {total}")
