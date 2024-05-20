import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

import numpy as np

# Part 1


def difference_last(arr: np.ndarray) -> int:
    if not any(arr): # Checks if all values are 0
        return arr[-1]
    return arr[-1] + difference_last(np.diff(arr, 1))


with open(filepath, 'r') as file:
    data: list[str] = file.readlines()

    total: int = 0
    for row in data:
        row_data: np.ndarray = np.array([int(n) for n in row.split(" ")])
        total += difference_last(row_data)

    print(f"Part 1: {total}")


# Part 2


def difference_first(arr: np.ndarray) -> int:
    if not any(arr):
        return arr[0]
    return arr[0] - difference_first(np.diff(arr, 1))


with open(filepath, "r") as file:
    data = file.readlines()

    total = 0
    for row in data:
        row_data = np.array([int(n) for n in row.split(" ")])
        total += difference_first(row_data)

    print(f"Part 2: {total}")
