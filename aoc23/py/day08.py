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
            print(line)
            left, right = line.split("=")
            maps[left.strip()] = tuple([x.strip() for x in right.replace("(", "").replace(")", "").split(",")])


    i = 0
    currents = [node for node in maps if node.endswith("A")]

    repeating = itertools.cycle(instructions)
    seens = set()
    while True:
        ins = 0 if next(repeating) == "L" else 1
        next_steps = [maps[cur][ins] for cur in currents]

        key = (tuple(next_steps), ins)
        if key in seens:
            breakpoint()
        print(next_steps)
        seens.add(key)
        i += 1
        if all(n.endswith("Z") for n in next_steps):
            break
        currents = next_steps


    print(i)

    #print(maps)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day08(examples("08"))
day08(inputs("08"))
