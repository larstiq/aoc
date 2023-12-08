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
    current = "AAA"

    repeating = itertools.cycle(instructions)
    while True:
        ins = 0 if next(repeating) == "L" else 1
        next_step = maps[current][ins]
        print(next_step)
        i += 1
        if next_step == "ZZZ":
            break
        current = next_step


    print(i)

    #print(maps)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day08(examples("08"))
day08(inputs("08"))
