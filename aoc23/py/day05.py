#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx


def day05(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    seeds = set()
    stage = "seed"

    current = set()
    next_state = set()
    with open(filename) as puzzlein:
        for line in puzzlein:
            #print(line)
            if line.startswith("seeds:"):
                seeds = { int(x) for x in line.split(":")[1].split() }
                next_state = seeds
            elif line == "\n":
                continue
            elif ":" in line and line.split(":")[0].split()[1] == "map":
                map_name = line.split(":")[0].split()[0]
                current = next_state
                next_state = set()
            elif line.strip() == "":
                continue
            else:
                dest, source, lengte = [int(x) for x in line.split()]
                for y in list(current):
                    if y in range(source, source + lengte):
                        next_state.add(dest + y - source) 
                        current.remove(y)

    print(current)
    print(next_state)

    print("part1:", part1)
    print("part2:", part2)


day05(examples("05"))
day05(inputs("05"))
