import os
import re

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

# Part 1


with open(filepath, "r") as file:
    total: int = 0
    for row in file.readlines():
        digits: list[str] = re.findall(r"\d", row)
        total += int(digits[0] + digits[-1])
    print(f"Part 1: {total}")


# Part 2


def get_digit(key: str) -> str:
    digits_map: dict[str, str] = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    return digits_map.get(key, key)


pattern: str = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"

with open(filepath, "r") as file:
    total = 0
    for row in file.readlines():
        digits = re.findall(pattern, row)
        total += int(get_digit(digits[0]) + get_digit(digits[-1]))
    print(f"Part 2: {total}")
