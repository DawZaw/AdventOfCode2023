from __future__ import annotations
import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

from typing import Self


class Vector:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Self) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Beam:
    position: Vector
    direction: Vector

    def __init__(self, position: Vector, direction: Vector) -> None:
        self.position = position
        self.direction = direction

    def move(self) -> None:
        self.position += self.direction

    def reflect(self, mirror: str) -> None:
        x: int = self.direction.x
        y: int = self.direction.y
        if mirror == chr(92):  # \ character
            self.direction.x = y
            self.direction.y = x
        elif mirror == "/":
            self.direction.x = -y
            self.direction.y = -x

    def split(self, splitter: str) -> list[Beam]:
        if splitter == "|":
            return [
                Beam(self.position, Vector(0, -1)),
                Beam(self.position, Vector(0, 1)),
            ]
        if splitter == "-":
            return [
                Beam(self.position, Vector(-1, 0)),
                Beam(self.position, Vector(1, 0)),
            ]
        return []

    def is_inbound(self, width: int, height: int) -> bool:
        return (
            self.position.x >= 0
            and self.position.x < width
            and self.position.y >= 0
            and self.position.y < height
        )


def count_energized(data: list[str], start_pos: Vector, direction: Vector) -> int:
    width: int = len(data[0])
    height: int = len(data)

    beams: list[Beam] = [Beam(start_pos, direction)]

    visited: dict[tuple[int, int], set[tuple[int, int]]] = {}
    while beams:
        beam: Beam = beams.pop(0)
        while beam.is_inbound(width, height):
            x: int = beam.position.x
            y: int = beam.position.y
            tile: str = data[y][x]
            curr_dir: tuple[int, int] = (beam.direction.x, beam.direction.y)

            if (y, x) in visited and curr_dir in visited[(y, x)]:
                # If beam direction has already been in current position
                # all future steps are already visited
                break
            else:
                visited[(y, x)] = visited.get((y, x), set([]))
                visited[(y, x)].add(curr_dir)

            if tile in r"\/":
                beam.reflect(tile)
            elif (tile == "|" and beam.direction.x != 0) or (
                tile == "-" and beam.direction.y != 0
            ):
                beams.extend(beam.split(tile))
                break

            beam.move()
    return len(visited)


with open(filepath, "r") as file:
    data: list[str] = [line.strip() for line in file.readlines()]

    # Part 1

    energized: int = count_energized(data, Vector(0, 0), Vector(1, 0))
    print(f"Part 1: {count_energized(data, Vector(0, 0), Vector(1, 0))}")

    # Part 2

    most_energized: int = 0
    positions: list[Vector] = []
    directions: list[Vector] = []
    for y in range(len(data)):
        # Add left column add direction to the right
        positions.append(Vector(0, y))
        directions.append(Vector(1, 0))
        # Add right column add direction to the left
        positions.append(Vector(len(data) - 1, y))
        directions.append(Vector(-1, 0))

    for x in range(len(data[0])):
        # Add top row add direction to the bottom
        positions.append(Vector(x, 0))
        directions.append(Vector(0, 1))
        # Add bottom row add direction to the top
        positions.append(Vector(x, len(data[0]) - 1))
        directions.append(Vector(0, -1))

    for pos, dir in zip(positions, directions):
        energized = count_energized(data, pos, dir)
        if energized > most_energized:
            most_energized = energized

    print(f"Part 2: {most_energized}")
