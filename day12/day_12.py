import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


from functools import cache


@cache
def count(condition: str, configuration: tuple[int, ...]) -> int:
    if not configuration:
        # if configuration groups are empty and condition string still has # signs
        # current result is wrong and we have to backtrack
        return 0 if "#" in condition else 1
    if not condition:
        # if condition string is empty and configuration still has groups left
        # current result is wrong and we have to backtrack
        return 1 if not configuration else 0

    result: int = 0
    match condition[0]:
        case ".":
            # if first character is . discard it and check again
            result += count(condition[1:], configuration)
        case "?":
            # replace ? with . and check again
            condition = "." + condition[1:]
            result += count(condition, configuration)

            # replace ? with # and check again
            condition = "#" + condition[1:]
            result += count(condition, configuration)
        case "#":
            current_slice: str = condition[: configuration[0]]
            remaining: int = len(condition)
            # check if configuration is shorter or equal to remaining condition
            # and all characters are either # or ?
            # and either there are no more characters after current slice
            # or character after current slice is . or ?
            if (
                configuration[0] <= remaining
                and "." not in current_slice
                and (
                    len(current_slice) == remaining
                    or condition[configuration[0]] in ".?"
                )
            ):
                # remove slice from condition string with extra space for . or ?
                # and remove first group from configuration
                result += count(condition[configuration[0] + 1 :], configuration[1:])

    return result


with open(filepath, "r") as file:
    data: list[str] = file.readlines()

    # Part 1

    total: int = 0
    for row in data:
        condition: str = row.split()[0]
        configuration: tuple[int, ...] = eval(row.split()[1])
        total += count(condition, configuration)
    print(f"Part 1: {total}")

    # Part 2

    total = 0
    for row in data:
        condition = "?".join([row.split()[0]] * 5)
        configuration = eval((row.split()[1] + ",") * 5)
        total += count(condition, configuration)
    print(f"Part 2: {total}")
