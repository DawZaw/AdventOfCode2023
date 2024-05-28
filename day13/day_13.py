import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


import numpy as np


def process_row(row: str) -> list[str]:
    return list(row.strip().replace("#", "1").replace(".", "0"))


def process_data(data: list[str]) -> list[np.ndarray]:
    result: list[np.ndarray] = []
    start: int = 0
    # Concatenate ["\n"] to data, to include last pattern
    for stop, row in enumerate(data + ["\n"]):
        if row == "\n":
            result.append(
                np.array([process_row(row) for row in data[start:stop]], dtype=int)
            )
            start = stop + 1
    return result


def reflection(pattern: np.ndarray, vertical: bool = False, smudges: int = 0) -> int:
    if vertical:
        # Transpose matrix for vertical reflection lines
        pattern = pattern.T
    for i in range(pattern.shape[0] - 1):
        # Split matrix into top and bottom parts, flip top part to check for symmetry
        top: np.ndarray = np.flip(pattern[: i + 1], axis=0)
        bot: np.ndarray = pattern[i + 1 :]
        # Find min rows to avoid IndexError
        min_rows: int = min(top.shape[0], bot.shape[0])
        # If difference between top and bottom parts equals to number of smudges
        # then that is the symmetry line
        if np.count_nonzero(top[:min_rows] - bot[:min_rows]) == smudges:
            return i + 1
    return 0


with open(filepath, "r") as file:
    data: list[np.ndarray] = process_data(file.readlines())

    # Part 1

    total: int = 0
    for pattern in data:
        horizontal: int = reflection(pattern)
        vertical: int = reflection(pattern, vertical=True)
        total += horizontal * 100 + vertical
    print(f"Part 1: {total}")

    # Part 2

    total = 0
    for pattern in data:
        horizontal = reflection(pattern, smudges=1)
        vertical = reflection(pattern, vertical=True, smudges=1)
        total += horizontal * 100 + vertical
    print(f"Part 2: {total}")
