import os
import re

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


def get_distance(time: int, max_time: int) -> int:
    return (max_time - time) * time


def all_wins(max_time: int, record_distance: int) -> int:
    l_time: int = 0
    r_time: int = max_time
    c_time: int = (l_time + r_time) // 2
    while c_time not in [l_time, r_time]:
        if get_distance(c_time, max_time) < record_distance:
            l_time = c_time
        elif get_distance(c_time, max_time) > record_distance:
            r_time = c_time
        c_time = (l_time + r_time) // 2
    return 2 * (max_time // 2 - c_time) - 1 + (max_time % 2)


with open(filepath, "r") as file:
    data: list[str] = file.readlines()
    times: list[int] = [int(t) for t in re.findall(r"\d+", data[0])]
    distances: list[int] = [int(d) for d in re.findall(r"\d+", data[1])]

    # Part 1
    total: int = 1
    for t, d in zip(times, distances):
        total *= all_wins(t, d)

    print(f"Part 1: {total}")

    # Part 2
    time: int = int("".join(str(t) for t in times))
    distance: int = int("".join(str(d) for d in distances))

    print(f"Part 2: {all_wins(time, distance)}")
