#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools

class SeedRange(object):
    start: int
    end: int

def day05(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    seeds = set()
    stage = "seed"

    current = set()
    with open(filename) as puzzlein:
        for line in puzzlein:
            #print(line)
            if line.startswith("seeds:"):
                pair = []
                pre_seeds = [ int(x) for x in line.split(":")[1].split() ]
                for entry in pre_seeds:
                    if len(pair) < 2:
                        pair.append(entry)
                    else:
                        seeds.add((pair[0], pair[0] + pair[1] - 1))
                        pair = [entry]

                print("pair", pair)
                seeds.add((pair[0], pair[0] + pair[1] -1))
                next_state = seeds
            elif line == "\n":
                continue
            elif ":" in line and line.split(":")[0].split()[1] == "map":
                map_name = line.split(":")[0].split()[0]
                #assert current == set()
                #breakpoint()
                print("Pre", map_name, current, next_state)
                current |= next_state
                next_state = set()
                print("Swapped", map_name, current, next_state)
            elif line.strip() == "":
                continue
            else:
                dest, source, lengte = [int(x) for x in line.split()]

                candidates = set()
                #assert current != set()
                candidates |= current
                print(map_name, dest, source, lengte)
                while len(candidates) > 0:
                    
                    seed_range = candidates.pop()
                    intersection = max(source, seed_range[0]), min(source + lengte, seed_range[1])
                    #print(f"Intersecting {(seed_range[0], seed_range[1])} with {(source, source + lengte)} gets {intersection}") 
                    shift = dest - source
                    if intersection == seed_range:
                        current.remove(seed_range)
                        next_state.add((shift + seed_range[0], shift + seed_range[1]))
                        print(current, next_state)
                    elif intersection[0] <= intersection[1]:
                        print("SPLIT!")
                        #breakpoint()
                        current.remove(seed_range)
                        next_state.add((shift + intersection[0], shift + intersection[1]))

                        if intersection[0] > seed_range[0]:
                            #current.add((dest + seed_range[0] - source, dest + intersection[0] - seed_range[0] - source))
                            current.add((shift + seed_range[0], shift + min(seed_range[1], intersection[0] - 1)))
                        if intersection[1] < seed_range[1]:
                            current.add((shift + max(intersection[1] + 1, seed_range[0]), shift + seed_range[1]))

                        print(current, next_state)
                    else:
                        pass




    print(current)
    print(next_state)
    breakpoint()

    print("part1:", part1)
    print("part2:", part2)


day05(examples("05"))
#day05(inputs("05"))
