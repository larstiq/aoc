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

def day05(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    seeds = []
    seeds1 = []
    seeds2 = []
    stage = "seed"

    current = []
    next_state = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            if line.startswith("seeds:"):
                pair = []
                pre_seeds = [ int(x) for x in line.split(":")[1].split() ]
                for entry in pre_seeds:
                    if len(pair) < 2:
                        pair.append(entry)
                    else:
                        seeds.append(Interval(pair[0], pair[0] + pair[1] - 1))
                        pair = [entry]

                #print("pair", pair)
                seeds.append(Interval(pair[0], pair[0] + pair[1] -1))
                next_state = seeds
            elif line == "\n":
                continue
            elif ":" in line and line.split(":")[0].split()[1] == "map":
                map_name = line.split(":")[0].split()[0]
                #print("Pre", map_name, current, next_state)
                aap = next_state + current
                #assert sum(map(lambda x: len(x) + 1, seeds)) == sum(map(lambda x: len(x) + 1, aap))
                current = aap
                next_state = []
                #print("Swapped", map_name, current, next_state)
            elif line.strip() == "":
                continue
            else:
                dest, source, lengte = [int(x) for x in line.split()]

                #print(map_name, dest, source, lengte)
                assert lengte > 0
                out_range = Interval(source, source + lengte - 1)
                carry = []
                while len(current) > 0:
                    
                    seed_range = current.pop()
                    offset = dest - source
                    # Skip no intersections
                    if seed_range.upper < out_range.lower or seed_range.lower > out_range.upper:
                        carry.append(seed_range)
                        continue
                    elif seed_range.upper == out_range.lower:
                        next_state.append(shift(Interval(seed_range.upper, seed_range.upper), offset))
                        assert seed_range.lower < seed_range.upper
                        carry.append(Interval(seed_range.lower, seed_range.upper - 1))
                        continue
                    elif seed_range.lower == out_range.upper:
                        next_state.append(shift(Interval(seed_range.lower, seed_range.lower), offset))
                        assert seed_range.lower < seed_range.upper
                        carry.append(Interval(seed_range.lower + 1, seed_range.upper))
                        continue

                    intersection = seed_range.intersection(out_range)
                    next_state.append(shift(intersection, offset))

                    #print(f"Found intersection {(intersection.start, intersection.stop)} of {(out_range.start, out_range.stop)} and {(seed_range.start, seed_range.stop)}")

                    if intersection == seed_range:
                        continue

                    for remainder in seed_range - intersection:
                        if remainder.left == OPEN:
                            current.append(Interval(remainder.lower + 1, remainder.upper))
                        elif remainder.right == OPEN:
                            current.append(Interval(remainder.lower, remainder.upper - 1))
                        else:
                            breakpoint()

                current += carry


    print(current)
    print(next_state)
    starts = {interval.lower for interval in current}
    startstwee = {interval.lower for interval in next_state}
    part2 = min(startstwee)

    if str(filename).endswith("inputs/05"):
        #assert part1 == 662197086
        assert part2 == 52510809
    # breakpoint()

    #print("part1:", part1)
    print("part2:", part2)


day05(examples("05"))
import time
start = time.time()
day05(inputs("05"))
end = time.time()
print(end - start)
