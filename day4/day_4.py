import os
import re

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

# Part 1


def count_hits(card: str) -> int:
    tmp: list[str] = re.sub(r"Card.+\d+:", "", card).split("|")
    winning: set[str] = set(re.findall(r"\d+", tmp[0]))
    choice: set[str] = set(re.findall(r"\d+", tmp[1]))
    count: int = len(choice.intersection(winning))
    return count


with open(filepath, "r") as file:
    total: int = 0
    for card in file.readlines():
        hits: int = count_hits(card)
        total += 2 ** (hits - 1) if hits else 0
    print(f"Part 1: {total}")


# Part 2

with open(filepath, "r") as file:
    cards = file.readlines()
    card_winnings = [1] * len(cards)
    for i, card in enumerate(cards):
        count = count_hits(card)
        for c in range(i + 1, i + count + 1):
            card_winnings[c] += card_winnings[i]
    print(f"Part 2: {sum(card_winnings)}")
