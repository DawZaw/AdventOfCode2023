from __future__ import annotations
import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


import re
from typing import Literal, TypeAlias, Any, cast


Category: TypeAlias = Literal["x", "m", "a", "s"]
Operator: TypeAlias = Literal["<", ">"]

# Part 1


class Rule:
    category: Category | None
    operator: Operator | None
    value: int | None
    destination: str
    # Default is a rule which contains only destination
    is_default: bool

    def __init__(self, rule: str) -> None:
        self.category = None
        self.operator = None
        self.value = None
        self.destination = rule
        self.is_default = True

        self._parse(rule)

    def _parse(self, rule: str) -> None:
        pattern: str = r"(\w)([<>])(\d+):(\w+)"
        match: list[Any] = re.findall(pattern, rule)
        if match:
            match = match[0]
            self.category = cast(Category, match[0])
            self.operator = cast(Operator, match[1])
            self.value = int(match[2])
            self.destination = match[3]
            self.is_default = False

    def get_destination(self) -> str:
        return self.destination

    def compare_part(self, part: Part) -> bool:
        # Return True if part value satisfies rule's comparison or rule is default
        if self.is_default:
            return True

        assert self.category is not None
        part_value: int = part.get_value(self.category)
        return eval(f"{part_value}{self.operator}{self.value}") or self.is_default

    def __repr__(self) -> str:
        if self.is_default:
            return self.destination
        return f"{self.category}{self.operator}{self.value}:{self.destination}"


class Part:
    x: int
    m: int
    a: int
    s: int

    def __init__(self, rating: str) -> None:
        self.x, self.m, self.a, self.s = self._parse(rating)

    def _parse(self, rating: str) -> list[int]:
        return [int(n) for n in re.findall(r"\d+", rating)]

    def get_value(self, category: Category) -> int:
        if category == "x":
            return self.x
        elif category == "m":
            return self.m
        elif category == "a":
            return self.a
        elif category == "s":
            return self.s

    def get_total(self) -> int:
        return self.x + self.m + self.a + self.s

    def validate(self, workflows: dict[str, list[Rule]]) -> int:
        current_workflow: list[Rule] = workflows["in"]
        rule_idx: int = 0
        while True:
            rule: Rule = current_workflow[rule_idx]
            if rule.compare_part(self):
                destination: str = rule.get_destination()
                if destination == "A":
                    return self.get_total()
                elif destination == "R":
                    return 0
                else:
                    current_workflow = workflows[destination]
                    rule_idx = 0
            else:
                rule_idx += 1

    def __repr__(self) -> str:
        return f"x={self.x},m={self.m},a={self.a},s={self.s}"


def parse_workflows(workflows: list[str]) -> dict[str, list[Rule]]:
    workflow_map: dict[str, list[Rule]] = {}

    pattern: str = r"(\w+){(.*)}"
    for workflow in workflows:
        key: str
        rules: str
        key, rules = re.findall(pattern, workflow)[0]
        workflow_map[key] = [Rule(rule) for rule in rules.split(",")]

    return workflow_map


# Part 2


from functools import reduce


def get_total(data: list[int]) -> int:
    return reduce(lambda x, y: x * y, data)


def bisect(span: tuple[int, int], value: int) -> tuple[tuple[int, int], ...]:
    a: tuple[int, int]
    b: tuple[int, int]
    if span[0] < value:
        if span[1] < value:
            a = span
            b = (0, 0)
        else:
            a = (span[0], value - 1)
            b = (value - 1, span[1])
    else:
        a = (0, 0)
        b = span
    return a, b


def range_diff(span: tuple[int, int]) -> int:
    return abs(span[0] - span[1])


def get_combinations(
    workflows: dict[str, list[Rule]],
    values_range: dict[str, tuple[int, int]],
    destination: str,
) -> int:
    if destination == "A":
        return get_total([range_diff(vr) for vr in values_range.values()])
    elif destination == "R":
        return 0

    workflow: list[Rule] = workflows[destination]
    total: int = 0

    for rule in workflow:
        if rule.is_default:
            total += get_combinations(workflows, values_range, rule.destination)
        else:
            new_range: tuple[int, int]
            remaining: tuple[int, int]

            assert rule.value is not None
            value: int = rule.value
            category: Category = cast(Category, rule.category)

            if rule.operator == "<":
                new_range, remaining = bisect(values_range[category], value)

            elif rule.operator == ">":
                remaining, new_range = bisect(values_range[category], value + 1)

            new_values_range = values_range.copy()
            new_values_range[category] = new_range
            values_range[category] = remaining
            total += get_combinations(workflows, new_values_range, rule.destination)

    return total


with open(filepath, "r") as file:
    data: list[str] = file.read().split("\n\n")

    to_parse: list[str] = [line for line in data[0].split()]
    workflows: dict[str, list[Rule]] = parse_workflows(to_parse)
    parts: list[Part] = [Part(part) for part in data[1].split()]

    total: int = 0
    for part in parts:
        total += part.validate(workflows)

    print(f"Part 1: {total}")

    values_range: dict[str, tuple[int, int]] = {
        "x": (0, 4000),
        "m": (0, 4000),
        "a": (0, 4000),
        "s": (0, 4000),
    }

    total_combinations: int = get_combinations(workflows, values_range, "in")
    print(f"Part 2: {total_combinations}")
