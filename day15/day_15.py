import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


import re
from collections import OrderedDict, defaultdict


def hash_step(step: str) -> int:
    result: int = 0
    for char in step:
        result += ord(char)
        result *= 17
        result %= 256
    return result


def create_boxes(steps: list[str]) -> dict[int, OrderedDict[str, int]]:
    boxes: dict[int, OrderedDict[str, int]] = defaultdict(OrderedDict[str, int])
    for step in steps:
        match: list[str] = re.findall(r"(.*)(=|-)(\d?)", step)[0]
        label: str = match[0]
        operator: str = match[1]
        if match[2]:
            value: int = int(match[2])

        box_nr: int = hash_step(label)

        if operator == "=":
            boxes[box_nr][label] = value
        elif operator == "-" and label in boxes[box_nr]:
            boxes[box_nr].pop(label)
    return boxes


def get_boxes_power(boxes: dict[int, OrderedDict[str, int]]) -> int:
    result: int = 0
    for nr, box in boxes.items():
        for i, val in enumerate(box.values()):
            box_value: int = (nr + 1) * (i + 1) * val
            result += box_value
    return result


with open(filepath, "r") as file:
    data: str = file.read().strip()
    steps: list[str] = data.split(",")

    # Part 1

    total: int = 0
    for step in steps:
        total += hash_step(step)

    print(f"Part 1: {total}")

    # Part 2

    boxes: dict[int, OrderedDict[str, int]] = create_boxes(steps)
    total = get_boxes_power(boxes)

    print(f"Part 2: {total}")
