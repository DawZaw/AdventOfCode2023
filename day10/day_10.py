import os

from collections import deque

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


def get_start_pos(pipes: list[str]) -> tuple[int, int]:
    for i, row in enumerate(pipes):
        if "S" in row:
            return (i, row.index("S"))
    return (-1, -1)


def north_is_valid(
    pipes: list[str], row: int, col: int, dist_map: dict[tuple[int, int], int]
) -> bool:
    return row >= 0 and (row, col) not in dist_map and pipes[row][col] in "|7F"


def south_is_valid(
    pipes: list[str], row: int, col: int, dist_map: dict[tuple[int, int], int]
) -> bool:
    n: int = len(pipes)
    return row <= n and (row, col) not in dist_map and pipes[row][col] in "|JL"


def east_is_valid(
    pipes: list[str], row: int, col: int, dist_map: dict[tuple[int, int], int]
) -> bool:
    n: int = len(pipes)
    return col <= n and (row, col) not in dist_map and pipes[row][col] in "-J7"


def west_is_valid(
    pipes: list[str], row: int, col: int, dist_map: dict[tuple[int, int], int]
) -> bool:
    return col >= 0 and (row, col) not in dist_map and pipes[row][col] in "-LF"


def validate_connections(
    pipes: list[str], row: int, col: int, dist_map: dict[tuple[int, int], int]
) -> list[tuple[int, int]]:
    valid_paths: list[tuple[int, int]] = []
    current: str = pipes[row][col]
    match current:
        case "|":
            if north_is_valid(pipes, row - 1, col, dist_map):
                valid_paths.append((row - 1, col))
            if south_is_valid(pipes, row + 1, col, dist_map):
                valid_paths.append((row + 1, col))
        case "-":
            if east_is_valid(pipes, row, col + 1, dist_map):
                valid_paths.append((row, col + 1))
            if west_is_valid(pipes, row, col - 1, dist_map):
                valid_paths.append((row, col - 1))
        case "L":
            if north_is_valid(pipes, row - 1, col, dist_map):
                valid_paths.append((row - 1, col))
            if east_is_valid(pipes, row, col + 1, dist_map):
                valid_paths.append((row, col + 1))
        case "J":
            if north_is_valid(pipes, row - 1, col, dist_map):
                valid_paths.append((row - 1, col))
            if west_is_valid(pipes, row, col - 1, dist_map):
                valid_paths.append((row, col - 1))
        case "7":
            if south_is_valid(pipes, row + 1, col, dist_map):
                valid_paths.append((row + 1, col))
            if west_is_valid(pipes, row, col - 1, dist_map):
                valid_paths.append((row, col - 1))
        case "F":
            if south_is_valid(pipes, row + 1, col, dist_map):
                valid_paths.append((row + 1, col))
            if east_is_valid(pipes, row, col + 1, dist_map):
                valid_paths.append((row, col + 1))
        case "S":
            if north_is_valid(pipes, row - 1, col, dist_map):
                valid_paths.append((row - 1, col))
            if south_is_valid(pipes, row + 1, col, dist_map):
                valid_paths.append((row + 1, col))
            if east_is_valid(pipes, row, col + 1, dist_map):
                valid_paths.append((row, col + 1))
            if west_is_valid(pipes, row, col - 1, dist_map):
                valid_paths.append((row, col - 1))
    return valid_paths


def traverse(pipes: list[str], row: int, col: int) -> dict[tuple[int, int], int]:
    dist_map: dict[tuple[int, int], int] = {}
    queue: deque = deque(validate_connections(pipes, row, col, dist_map))

    dist = 1
    while queue:
        current: tuple[int, int] = queue.popleft()
        dist_map[current] = dist
        curr_row: int = current[0]
        curr_col: int = current[1]
        queue.extend(validate_connections(pipes, curr_row, curr_col, dist_map))
        dist += 1
    return dist_map


with open(filepath, "r") as file:
    data: list[str] = file.readlines()

    start: tuple[int, int] = get_start_pos(data)
    dist_map: dict[tuple[int, int], int] = traverse(data, start[0], start[1])
    max_dist: int = int(max(dist_map.values()) / 2)
    print(f"Part 1: {max_dist}")
