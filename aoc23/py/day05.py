#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools
Interval = pd.RangeIndex

def day05(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    seeds = []
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

                print("pair", pair)
                seeds.append(Interval(pair[0], pair[0] + pair[1] -1))
                next_state = seeds
            elif line == "\n":
                continue
            elif ":" in line and line.split(":")[0].split()[1] == "map":
                map_name = line.split(":")[0].split()[0]
                print("Pre", map_name, current, next_state)
                # Unchanged stays
                #breakpoint()
                aap = next_state + current
                assert sum(map(lambda x: len(x) + 1, seeds)) == sum(map(lambda x: len(x) + 1, aap))
                current = aap
                next_state = []
                print("Swapped", map_name, current, next_state)
            elif line.strip() == "":
                continue
            else:
                dest, source, lengte = [int(x) for x in line.split()]

                print(map_name, dest, source, lengte)
                assert lengte > 0
                out_range = Interval(source, source + lengte - 1)
                carry = []
                while len(current) > 0:
                    
                    seed_range = current.pop()
                    # Skip no intersections
                    if seed_range.stop < out_range.start or seed_range.start > out_range.stop:
                        carry.append(seed_range)
                        continue
                    elif seed_range.stop == out_range.start:
                        next_state.append(shift + Interval(seed_range.stop, seed_range.stop))
                        # TODO: assert single item interval
                        carry.append(Interval(seed_range.start, seed_range.stop - 1))
                        continue
                    elif seed_range.start == out_range.stop:
                        next_state.append(shift + Interval(seed_range.start, seed_range.start))
                        carry.append(Interval(seed_range.start + 1, seed_range.stop))
                        continue

                    intersection = seed_range.intersection(out_range)
                    shift = dest - source
                    next_state.append(shift + intersection)

                    print(f"Found intersection {(intersection.start, intersection.stop)} of {(out_range.start, out_range.stop)} and {(seed_range.start, seed_range.stop)}")

                    if intersection.equals(seed_range):
                        continue

                    left_size = right_size = 0
                    if intersection.start > seed_range.start:
                        left = Interval(seed_range.start, min(intersection.start - 1, seed_range.stop))
                        current.append(left)
                        left_size = len(left) + 1
                        print(f"    left {(left.start, left.stop, len(left))} of {(out_range.start, out_range.stop)} and {(seed_range.start, seed_range.stop)}")
                    if intersection.stop < seed_range.stop:
                        right = Interval(max(seed_range.start, intersection.stop + 1), seed_range.stop)
                        current.append(right)
                        right_size = len(right) + 1
                        print(f"    right {(right.start, right.stop, len(right))} of {(out_range.start, out_range.stop)} and {(seed_range.start, seed_range.stop)}")

                    assert left_size + right_size + len(intersection) + 1 == len(seed_range) + 1

                current += carry


    print(current)
    print(next_state)
    starts = {interval.start for interval in current}
    startstwee = {interval.start for interval in next_state}
    part2 = min(starts)
    breakpoint()

    print("part1:", part1)
    print("part2:", part2)


day05(examples("05"))
day05(inputs("05"))
