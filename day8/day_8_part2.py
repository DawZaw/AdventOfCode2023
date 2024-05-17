import os
import re
import math
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

    origins: list[str] = [k for k in node_map.keys() if k[2] == "A"]
    n: int = len(origins)
    steps: list[int] = [0] * n
    for i in range(n):
        for dir in cycle(directions):
            current: str = origins[i]
            if current[2] == "Z":
                break
            match dir:
                case "R":
                    origins[i] = node_map[current]["right"]
                case "L":
                    origins[i] = node_map[current]["left"]
            steps[i] += 1

    lcm: int = steps[0]
    for i in range(1, n):
        lcm = math.lcm(lcm, steps[i])
    print(lcm)
