#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools
from portion import closed as Interval, OPEN


def shift(interval, offset):
    return Interval(interval.lower + offset, interval.upper + offset)


def map_intervals(dest, source, lengte, current, next_state):
    out_range = Interval(source, source + lengte - 1)

    carry = set()
    while len(current) > 0:
        seed_range = current.pop()
        offset = dest - source
        # Skip no intersections
        if seed_range.upper < out_range.lower or seed_range.lower > out_range.upper:
            # No intersection, put it to the side for now
            carry.add(seed_range)
            continue

        intersection = seed_range.intersection(out_range)
        next_state.add(shift(intersection, offset))

        if intersection == seed_range:
            continue

        for remainder in seed_range - intersection:
            if remainder.left == OPEN:
                current.add(Interval(remainder.lower + 1, remainder.upper))
            elif remainder.right == OPEN:
                current.add(Interval(remainder.lower, remainder.upper - 1))
            else:
                breakpoint()

    current |= carry


def day05(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    current = {}
    current["part1"] = set()
    current["part2"] = set()
    next_state = {}
    next_state["part1"] = set()
    next_state["part2"] = set()
    with open(filename) as puzzlein:
        for line in puzzlein:
            if line.startswith("seeds:"):
                pair = []
                pre_seeds = [ int(x) for x in line.split(":")[1].split() ]
                next_state["part1"] = {Interval(x, x) for x in pre_seeds}
                next_state["part2"] = seeds2 = set()
                for entry in pre_seeds:
                    if len(pair) < 2:
                        pair.append(entry)
                    else:
                        seeds2.add(Interval(pair[0], pair[0] + pair[1] - 1))
                        pair = [entry]

                seeds2.add(Interval(pair[0], pair[0] + pair[1] -1))
            elif line == "\n":
                continue
            elif ":" in line and line.split(":")[0].split()[1] == "map":
                map_name = line.split(":")[0].split()[0]
                # If no mapping then input/output are the same number so continue with leftovers
                current["part1"] |= next_state["part1"]
                current["part2"] |= next_state["part2"]
                next_state["part1"] = set()
                next_state["part2"] = set()
            elif line.strip() == "":
                continue
            else:
                dest, source, lengte = [int(x) for x in line.split()]
                map_intervals(dest, source, lengte, current["part1"], next_state["part1"])
                map_intervals(dest, source, lengte, current["part2"], next_state["part2"])


    part1 = min(interval.lower for interval in next_state["part1"])
    part2 = min(interval.lower for interval in next_state["part2"])

    if str(filename).endswith("inputs/05"):
        assert part1 == 662197086
        assert part2 == 52510809

    print("part1:", part1)
    print("part2:", part2)


day05(examples("05"))
import time
start = time.time()
day05(inputs("05"))
end = time.time()
print(end - start)
