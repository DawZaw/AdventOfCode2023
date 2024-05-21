import os

from collections import deque

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

Coord = tuple[int, int]


def get_start_pos(pipes: list[str]) -> Coord:
    for i, row in enumerate(pipes):
        if "S" in row:
            return (i, row.index("S"))
    return (-1, -1)


def is_valid(
    pipes: list[str],
    row: int,
    col: int,
    dist_map: dict[Coord, int],
    direction: str,
) -> bool:
    width: int = len(pipes[0])
    height: int = len(pipes)
    return (
        row >= 0
        and row <= height
        and col <= width
        and col >= 0
        and (row, col) not in dist_map
        and pipes[row][col] in direction
    )


def validate_connections(
    pipes: list[str], row: int, col: int, dist_map: dict[Coord, int]
) -> list[Coord]:

    directions: dict[str, str] = {
        "north": "|7F",
        "south": "|JL",
        "east": "-J7",
        "west": "-LF",
    }

    valid_paths: list[Coord] = []
    current: str = pipes[row][col]
    match current:
        case "|":
            if is_valid(pipes, row - 1, col, dist_map, directions["north"]):
                valid_paths.append((row - 1, col))
            if is_valid(pipes, row + 1, col, dist_map, directions["south"]):
                valid_paths.append((row + 1, col))
        case "-":
            if is_valid(pipes, row, col + 1, dist_map, directions["east"]):
                valid_paths.append((row, col + 1))
            if is_valid(pipes, row, col - 1, dist_map, directions["west"]):
                valid_paths.append((row, col - 1))
        case "L":
            if is_valid(pipes, row - 1, col, dist_map, directions["north"]):
                valid_paths.append((row - 1, col))
            if is_valid(pipes, row, col + 1, dist_map, directions["east"]):
                valid_paths.append((row, col + 1))
        case "J":
            if is_valid(pipes, row - 1, col, dist_map, directions["north"]):
                valid_paths.append((row - 1, col))
            if is_valid(pipes, row, col - 1, dist_map, directions["west"]):
                valid_paths.append((row, col - 1))
        case "7":
            if is_valid(pipes, row + 1, col, dist_map, directions["south"]):
                valid_paths.append((row + 1, col))
            if is_valid(pipes, row, col - 1, dist_map, directions["west"]):
                valid_paths.append((row, col - 1))
        case "F":
            if is_valid(pipes, row + 1, col, dist_map, directions["south"]):
                valid_paths.append((row + 1, col))
            if is_valid(pipes, row, col + 1, dist_map, directions["east"]):
                valid_paths.append((row, col + 1))
        case "S":
            if is_valid(pipes, row - 1, col, dist_map, directions["north"]):
                valid_paths.append((row - 1, col))
            if is_valid(pipes, row + 1, col, dist_map, directions["south"]):
                valid_paths.append((row + 1, col))
            if is_valid(pipes, row, col + 1, dist_map, directions["east"]):
                valid_paths.append((row, col + 1))
            if is_valid(pipes, row, col - 1, dist_map, directions["west"]):
                valid_paths.append((row, col - 1))
    return valid_paths


def traverse(pipes: list[str], row: int, col: int) -> dict[Coord, int]:
    dist_map: dict[Coord, int] = {}
    queue: deque = deque(validate_connections(pipes, row, col, dist_map))

    path: list[Coord] = []
    dist: int = 1
    while queue:
        current: Coord = queue.popleft()
        path.append(current)
        dist_map[current] = dist
        curr_row: int = current[0]
        curr_col: int = current[1]
        queue.extend(validate_connections(pipes, curr_row, curr_col, dist_map))
        dist += 1
    return dist_map


with open(filepath, "r") as file:
    data: list[str] = file.readlines()

    # Part 1
    start: Coord = get_start_pos(data)
    dist_map: dict[Coord, int] = traverse(data, start[0], start[1])
    dist_map[start] = 0
    max_dist: int = int(max(dist_map.values()) / 2)
    print(f"Part 1: {max_dist}")

    # Part 2
    total: int = 0
    for row, row_data in enumerate(data):
        inside: bool = False
        for col, symbol in enumerate(row_data):
            point_on_path: bool = (row, col) in dist_map
            if inside and not point_on_path:
                total += 1
            if point_on_path and symbol in "|7F":
                inside = not inside

    print(f"Part 2 {total}")
