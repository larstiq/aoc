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
    cycle_lengths = {}
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
                cycle_lengths[start] = path_length
                break

            seens.add(key)
            current = next_step

    if "AAA" in zpoints:
        part1 = zpoints["AAA"][0]


    #nexts = starts
    #path = [nexts]
    #while not all(n.endswith("Z") for n in nexts):
        #    nexts = [maps[c][0] for c in nexts]
        #path.append(nexts)

    # Example has multiple zpoints, but inputs doesn't
    #part2 = min(math.lcm(*[zs[0] for zs in zpoints.values()])
    choices = list(itertools.product(*zpoints.values()))
    lcms = [math.lcm(*c) for c in choices]

    if len(choices) == 1:
        part2 = math.lcm(*choices[0])
    else:
        # Chinese Remainder because 
        pass

    import sympy
    aargh = [cycle_lengths[start] - 1 for start in starts]
    chinese_lcms = [sympy.ntheory.modular.crt(aargh, c) for c in choices]
    min_lcm = min(lcm[0] for lcm in chinese_lcms if lcm is not None)

    part2 = min_lcm
    # TODO: check cycle_lengths coprime
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()

#day08(examples("08"))
day08(inputs("08"))
day08("counterexamples/08")
