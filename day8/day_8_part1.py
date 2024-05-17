import os
import re
from itertools import cycle

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


def create_map(data: list[str]) -> dict[str, dict[str, str]]:
    node_map: dict[str, dict[str, str]] = {}
    for row in data:
        origin: str
        left: str
        right: str
        origin, left, right = re.findall(r"\w+", row)
        node_map[origin] = {}
        node_map[origin]["left"] = left
        node_map[origin]["right"] = right
    return node_map

with open(filepath, "r") as file:
    data: list[str] = file.readlines()
    directions: str = data[0].strip()
    node_map: dict[str, dict[str, str]] = create_map(data[2:])
    
    steps: int = 0
    current: str = "AAA"
    for dir in cycle(directions):
        if current == "ZZZ":
            break
        match dir:
            case "R":
                current = node_map[current]["right"]
            case "L":
                current = node_map[current]["left"]
        steps += 1

    print(f"Part 1: {steps}")
