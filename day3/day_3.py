import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

SIGNS: str = "*=-%&@$/+#"

# Part 1


def neighbours(arr: list[str], row: int, col: int) -> bool:
    for x in range(-1, 2):
        for y in range(-1, 2):
            try:
                n: str = arr[row + x][col + y]
            except IndexError:
                continue
            if n in SIGNS:
                return True
    return False


with open(filepath, "r") as file:
    engine: list[str] = file.readlines()
    total: int = 0
    for x, row in enumerate(engine):
        adj_sign: list[bool] = []
        number: str = ""
        for y, char in enumerate(row):
            if char.isnumeric():
                number += char
                adj_sign.append(neighbours(engine, x, y))
            elif number and char in SIGNS + ".":
                if any(adj_sign):
                    total += int(number)
                number = ""
                adj_sign.clear()
    print(f"Part 1: {total}")

# Part 2


def mult_neighbours(arr: list[str], row: int, col: int) -> int:
    star_neigh: list[int] = []
    for i in range(-1, 2):
        left: int = 1
        right: int = 1
        current_row: str = arr[row - i]
        while current_row[col - left].isnumeric():
            left += 1
        while current_row[col + right].isnumeric():
            right += 1
        numbers: list[str] = (
            current_row[col - left + 1 : col + right].replace("*", ".").split(".")
        )
        for number in numbers:
            if number:
                star_neigh.append(int(number))
    if len(star_neigh) == 2:
        return star_neigh[0] * star_neigh[1]
    return 0


with open(filepath, "r") as file:
    engine = file.readlines()
    total = 0
    for x, row in enumerate(engine):
        for y, char in enumerate(row):
            if char == "*":
                total += mult_neighbours(engine, x, y)
    print(f"Part 2: {total}")
