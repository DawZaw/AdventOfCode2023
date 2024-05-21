from day_10 import path, filepath, Coord
from day_10 import traverse, get_start_pos


def ascii() -> None:
    """Create ascii map of pipes with highlighted elements inside loop"""

    symbols: dict[str, str] = {
        "S": "S",
        "|": "│",
        "-": "─",
        "L": "└",
        "F": "┌",
        "J": "┘",
        "7": "┐",
        ".": ".",
    }

    with open(filepath, "r") as file:
        data: list[str] = file.readlines()

        start: Coord = get_start_pos(data)
        dist_map: dict[Coord, int] = traverse(data, start[0], start[1])
        dist_map[start] = 0

        with open(path + "\\ascii.txt", "w", encoding="UTF-8") as output:
            for row, row_data in enumerate(data):
                inside: bool = False
                line: str = ""
                for col, symbol in enumerate(row_data.strip()):
                    char: str = symbols[symbol]
                    point_on_path: bool = (row, col) in dist_map
                    if point_on_path:
                        if symbol in "|7F":
                            inside = not inside
                    else:
                        char = "O" if inside else " "
                    line += char
                output.write(line + "\n")


if __name__ == "__main__":
    ascii()
