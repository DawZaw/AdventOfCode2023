import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


from typing import TypeAlias, Literal, cast


Point: TypeAlias = tuple[int, int]
Direction: TypeAlias = Literal["U", "R", "D", "L"]


def parse_data(data: list[str]) -> tuple[list[Direction], list[int], list[str]]:
    directions: list[Direction] = []
    steps: list[int] = []
    colors: list[str] = []

    for line in data:
        tmp: list[str] = line.split(" ")
        directions.append(cast(Direction, tmp[0]))
        steps.append(int(tmp[1]))
        colors.append(tmp[2][2:-1])  # Leave out '(#)' characters

    return directions, steps, colors


def get_points(directions: list[Direction], steps: list[int]) -> list[Point]:
    points: list[Point] = [(0, 0)]
    prev_point_idx: int = 0

    for direction, step in zip(directions, steps):
        x: int = points[prev_point_idx][0]
        y: int = points[prev_point_idx][1]
        if direction == "R":
            points.append((x + step, y))
        elif direction == "L":
            points.append((x - step, y))
        elif direction == "U":
            points.append((x, y - step))
        elif direction == "D":
            points.append((x, y + step))
        prev_point_idx += 1

    return points[:-1]  # Drop last point which is the same as first (0, 0)


def shoelace(points: list[Point]) -> int:
    """
    Shoelace theorem is a formula for finding the area of a polygon
    given the coordinates of its vertices.
    """
    area: int = 0
    for i, point in enumerate(points):
        idx: int = (i + 1) % len(points)  # When at last point, wraps around to first
        area += (points[idx][0] + point[0]) * (points[idx][1] - point[1])
    return abs(area) // 2


def pick(area: int, boundary: int) -> int:
    """
    Pick's theorem expresses the area (A) of a polygon,
    whose vertices are lattice points in a coordinate plane
    based on number of points on the sides of polygon (B)
    and points inside (I).
    A = I + B/2 - 1
    By rearranging formula, we are able to get points inside polygon.
    I = A - B/2 + 1
    """
    return area - (boundary // 2) + 1


def parse_colors(colors: list[str]) -> tuple[list[Direction], list[int]]:
    directions: list[Direction] = []
    steps: list[int] = []

    dir_map: dict[str, Direction] = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }

    for color in colors:
        direction: Direction = dir_map[color[-1]]
        step: int = int(color[:-1], 16)

        directions.append(direction)
        steps.append(step)

    return directions, steps


with open(filepath, "r") as file:
    data: list[str] = [line.strip() for line in file.readlines()]

    directions: list[Direction]
    steps: list[int]
    colors: list[str]
    directions, steps, colors = parse_data(data)

    # Part 1

    points: list[Point] = get_points(directions, steps)
    area: int = shoelace(points)
    boundary: int = sum(steps)
    interior: int = pick(area, boundary)
    total: int = boundary + interior

    print(f"Part 1: {total}")

    # Part 2

    directions, steps = parse_colors(colors)

    points = get_points(directions, steps)
    area = shoelace(points)
    boundary = sum(steps)
    interior = pick(area, boundary)
    total = boundary + interior

    print(f"Part 2: {total}")
