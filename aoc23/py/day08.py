#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools

def day08(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    maps = {}
    with open(filename) as puzzlein:
        instructions = puzzlein.readline().strip()
        puzzlein.readline()
        for line in puzzlein:
            left, right = line.split("=")
            maps[left.strip()] = tuple([x.strip() for x in right.replace("(", "").replace(")", "").split(",")])


    starts = [node for node in maps if node.endswith("A")]

    zpoints = defaultdict(list)
    for start in starts:
        path_length = 0
        nth_instruction = 0
        seens = set()
        current = start
        while True:
            repeating = instructions[nth_instruction]
            ins = 0 if repeating == "L" else 1
            next_step = maps[current][ins]

            path_length += 1
            nth_instruction += 1
            nth_instruction %= len(instructions)

            if next_step.endswith("Z"):
                zpoints[start].append(path_length)

            # We might be back at the same node but perhaps not in the same
            # position in the instructions so the unique cycle might still be
            # longer.
            key = (current, nth_instruction)
            if key in seens:
                break

            seens.add(key)
            current = next_step

    if "AAA" in zpoints:
        part1 = zpoints["AAA"][0]
    # Example has multiple zpoints, but inputs doesn't
    part2 = math.lcm(*[zs[0] for zs in zpoints.values()])
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day08(examples("08"))
day08(inputs("08"))
