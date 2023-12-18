#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

TURNS = {
    UP: [LEFT, RIGHT],
    DOWN: [RIGHT, LEFT],
    LEFT: [UP, DOWN],
    RIGHT: [
        DOWN,
        UP,
    ],
}

DIGS = {
    "U": UP,
    "D": DOWN,
    "R": RIGHT,
    "L": LEFT
}

def day18(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(line.strip())

    df = pd.DataFrame(data)

    dug = pd.DataFrame(data=False, index=range(-2000, 2000), columns=range(-2000, 2000))

    start = (0, 0)
    pos = start
    dug[0][0] = True
    for instructions in data:
        letter, amount, colour = instructions.split()
        amount = int(amount)
        direction = DIGS[letter]
        for step in range(1, amount + 1):
            pos = pos[0] + direction[0], pos[1] + direction[1]
            dug[pos[1]][pos[0]] = True
            

    print(dug)
    DUG = scipy.ndimage.binary_fill_holes(dug)
        

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day18(examples("18"))
day18(inputs("18"))
