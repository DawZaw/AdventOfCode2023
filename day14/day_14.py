import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

from copy import deepcopy
from typing import Literal


def get_total_score(data: list[list[str]]) -> int:
    width: int = len(data[0])
    height: int = len(data)

    current_scores: list[int] = [0] * width
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == "O":
                current_scores[j] += height - i
    return sum(current_scores)


def move_row_wise(data: list[list[str]], dir: Literal["n", "s"]) -> list[list[str]]:
    width: int = len(data[0])

    if dir == "n":
        columns_idx: list[int] = [0] * width
        order: range = range(len(data))
        idx: int = 1
    elif dir == "s":
        columns_idx = [len(data) - 1] * width
        order = range(len(data) - 1, -1, -1)
        idx = -1

    for i in order:
        for j in range(width):
            if data[i][j] == "O":
                data[i][j] = "."
                data[columns_idx[j]][j] = "O"
                columns_idx[j] += idx
            elif data[i][j] == "#":
                columns_idx[j] = i + idx
    return data


def move_column_wise(data: list[list[str]], dir: Literal["w", "e"]) -> list[list[str]]:
    height: int = len(data)
    width: int = len(data[0])

    if dir == "w":
        rows_idx: list[int] = [0] * height
        order: range = range(width)
        idx: int = 1
    elif dir == "e":
        rows_idx = [len(data) - 1] * height
        order = range(width - 1, -1, -1)
        idx = -1

    for i in range(height):
        for j in order:
            if data[i][j] == "O":
                data[i][j] = "."
                data[i][rows_idx[i]] = "O"
                rows_idx[i] += idx
            elif data[i][j] == "#":
                rows_idx[i] = j + idx
    return data


def tilt_north(data: list[list[str]]) -> list[list[str]]:
    return move_row_wise(data, "n")


def tilt_south(data: list[list[str]]) -> list[list[str]]:
    return move_row_wise(data, "s")


def tilt_east(data: list[list[str]]) -> list[list[str]]:
    return move_column_wise(data, "e")


def tilt_west(data: list[list[str]]) -> list[list[str]]:
    return move_column_wise(data, "w")


def cycle(data: list[list[str]]) -> list[list[str]]:
    data = tilt_north(data)
    data = tilt_west(data)
    data = tilt_south(data)
    data = tilt_east(data)
    return data


CYCLES: int = 1_000_000_000

with open(filepath, "r") as file:
    data: list[list[str]] = [list(line) for line in file.readlines()]
    tortoise: list[list[str]] = deepcopy(data)
    hare: list[list[str]] = deepcopy(data)

    # Part 1

    data = tilt_north(data)
    score: int = get_total_score(data)
    print(f"Part 1: {score}")

    # Part 2

    for i in range(CYCLES):
        score = get_total_score(tortoise)
        tortoise = cycle(tortoise)
        hare = cycle(hare)
        hare = cycle(hare)
        if tortoise == hare:
            print(f"Cycle repeats every {i}.")
            break

    print(f"Part 2: {score}")
