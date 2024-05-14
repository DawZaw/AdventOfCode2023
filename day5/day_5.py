import os
import re

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"

from collections import defaultdict
from typing import Any

SeedRange = tuple[int, int]
Almanac = dict[str, dict[SeedRange, int]]

# Part 1


def create_almanac(data: list[str]) -> Almanac:
    """
    Create almanac dict containing all categories and all ranges for each category
    example:
    seed-to-soil map:
    50 98 2
    almanac = {
        'seed-to-soil': {
            (98, 100): 50,
        }
    }
    """
    almanac: Almanac = defaultdict(dict[SeedRange, int])
    # Skip seed and first empty row
    for row in data[2:]:
        category: re.Match = re.match(r"\w+-to-\w+", row) or category
        try:
            dest, source, span = (int(x) for x in re.findall(r"\d+", row))
            src_range: SeedRange = (source, source + span)
            almanac[category[0]].update({src_range: dest})
        except ValueError as e:
            # Skip rows without numeric data
            pass
    return almanac


def difference(source: int, seed: int) -> int:
    """Calculate how far seed lies from source"""
    return seed - source


def get_value(almanac_cat: dict[SeedRange, int], seed: int) -> int:
    """Return destination value + difference if seed is in range else return seed"""
    for cat_range in almanac_cat.keys():
        source: int = cat_range[0]
        source_end: int = cat_range[1]
        if seed >= source and seed < source_end:
            return almanac_cat[cat_range] + difference(source, seed)
    return seed


def seed_to_location(almanac: Almanac, seed: int) -> int:
    seed = get_value(almanac["seed-to-soil"], seed)
    seed = get_value(almanac["soil-to-fertilizer"], seed)
    seed = get_value(almanac["fertilizer-to-water"], seed)
    seed = get_value(almanac["water-to-light"], seed)
    seed = get_value(almanac["light-to-temperature"], seed)
    seed = get_value(almanac["temperature-to-humidity"], seed)
    seed = get_value(almanac["humidity-to-location"], seed)
    return seed


with open(filepath, "r") as file:
    data: list[str] = file.readlines()
    seeds: list[int] = [int(x) for x in re.findall(r"\d+", data[0])]
    almanac: Almanac = create_almanac(data)

    locations: list[int] = [seed_to_location(almanac, seed) for seed in seeds]

    print(f"Part 1: {min(locations)}")

# Part 2


def split_range(src_range: SeedRange, map_range: SeedRange) -> list[SeedRange]:
    src_start: int = src_range[0]
    src_stop: int = src_range[1]
    map_start: int = map_range[0]
    map_stop: int = map_range[1]
    if src_start < map_start:
        if src_stop <= map_start:
            return [(src_start, src_stop)]
        elif src_stop > map_start and src_stop <= map_stop:
            return [(src_start, map_start), (map_start, src_stop)]
        elif src_stop > map_stop:
            return [
                (src_start, map_start),
                (map_start, map_stop),
                (map_stop, src_stop),
            ]
    elif src_start > map_start and src_start <= map_stop:
        if src_stop <= map_stop:
            return [(src_start, src_stop)]
        elif src_stop > map_stop:
            return [(src_start, map_stop), (map_stop, src_stop)]
    elif src_start > map_stop:
        return [(src_start, src_stop)]
    return [(src_start, src_stop)]


def reduce(arr: list[Any]) -> list[Any]:
    return list(set(arr))


def get_value_range(
    almanac_cat: dict[SeedRange, int], seed_ranges: list[SeedRange]
) -> list[SeedRange]:
    for cat_range in almanac_cat:
        for r in set(seed_ranges):
            seed_ranges += split_range(r, cat_range)
        seed_ranges = reduce(seed_ranges)
    for i, seed_range in enumerate(seed_ranges):
        st: int = get_value(almanac_cat, seed_range[0])
        en: int = get_value(almanac_cat, seed_range[1])
        seed_ranges[i] = (st, en)
    return seed_ranges


def seed_to_location_range(
    almanac: Almanac, seed_ranges: list[SeedRange]
) -> list[SeedRange]:
    seed_ranges = get_value_range(almanac["seed-to-soil"], seed_ranges)
    seed_ranges = get_value_range(almanac["soil-to-fertilizer"], seed_ranges)
    seed_ranges = get_value_range(almanac["fertilizer-to-water"], seed_ranges)
    seed_ranges = get_value_range(almanac["water-to-light"], seed_ranges)
    seed_ranges = get_value_range(almanac["light-to-temperature"], seed_ranges)
    seed_ranges = get_value_range(almanac["temperature-to-humidity"], seed_ranges)
    seed_ranges = get_value_range(almanac["humidity-to-location"], seed_ranges)
    return seed_ranges


with open(filepath, "r") as file:
    data = file.readlines()
    seeds = [int(x) for x in re.findall(r"\d+", data[0])]
    almanac = create_almanac(data)

    seed_ranges: list[SeedRange] = [
        (seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds) - 1, 2)
    ]
    locations_ranges: list[SeedRange] = seed_to_location_range(almanac, seed_ranges)

    print(f"Part 2: {min(locations_ranges)[1]}")
