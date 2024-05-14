import os
import re

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

# Part 1


def is_possible(count: int, color: str) -> bool:
    possible: bool = True
    match color:
        case "red":
            possible = count <= 12
        case "green":
            possible = count <= 13
        case "blue":
            possible = count <= 14
    return possible


pattern: str = r"\d+ green|\d+ red|\d+ blue"

with open(filepath, "r") as file:
    total: int = 0
    for i, row in enumerate(file.readlines()):
        pairs: list[str] = re.findall(pattern, row)
        for pair in pairs:
            split: list[str] = pair.split(" ")
            count: int = int(split[0])
            color: str = split[1]
            possible: bool = is_possible(count, color)
            if not possible:
                break
        total += (i + 1) * possible
    print(f"Part 1: {total}")


# Part 2

with open(filepath, "r") as file:
    total = 0
    for row in file.readlines():
        cubes: dict[str, int] = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        pairs = re.findall(pattern, row)
        for pair in pairs:
            split = pair.split(" ")
            count = int(split[0])
            color = split[1]
            cubes[color] = max(cubes[color], count)
        total += cubes["red"] * cubes["green"] * cubes["blue"]
    print(f"Part 2: {total}")
