import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

Coord = tuple[int, int]


def process_starmap(starmap: list[str]) -> tuple[list[Coord], dict[str, list[int]]]:
    stars: list[Coord] = []
    empty: dict[str, list[int]] = {
        "rows": [],
        "cols": [],
    }

    column_checker: list[int] = [0] * len(starmap[0])
    for r_idx, row in enumerate(starmap):
        row = row.strip()
        if len(set(row)) == 1:
            empty["rows"].append(r_idx)

        for c_idx, char in enumerate(row):
            if char == "#":
                column_checker[c_idx] += 1
                stars.append((r_idx, c_idx))

    empty["cols"] = [i for i, val in enumerate(column_checker) if val == 0]
    return stars, empty


def distance(s1: Coord, s2: Coord) -> int:
    return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])


def cross_empty_rows_cols(s1: Coord, s2: Coord, empty: dict[str, list[int]]) -> int:
    """
    Count how many ADDITIONAL empty rows and columns there are between two stars

    """
    total: int = 0
    min_row: int = min(s1[0], s2[0])
    max_row: int = max(s1[0], s2[0])
    min_col: int = min(s1[1], s2[1])
    max_col: int = max(s1[1], s2[1])
    for row in empty["rows"]:
        if min_row < row < max_row:
            total += 1
    for col in empty["cols"]:
        if min_col < col < max_col:
            total += 1
    return total


with open(filepath, "r") as file:
    data: list[str] = file.readlines()

    stars: list[Coord]
    empty: dict[str, list[int]]
    stars, empty = process_starmap(data)

    dist: int = 0
    dist_expanded: int = 0
    expand_mult: int = 1_000_000
    for i, star in enumerate(stars):
        for star2 in stars[i + 1 :]:
            d: int = distance(star, star2)
            extra_rows_cols: int = cross_empty_rows_cols(star, star2, empty)
            dist += d + extra_rows_cols
            # -1 because initial row and col are already counted
            dist_expanded += d + extra_rows_cols * (expand_mult - 1)
    print(f"Part 1: {dist}")
    print(f"Part 2: {dist_expanded}")
