#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict, deque, Counter
import time

import numpy as np
import re
import itertools

import networkx as nx
import sympy

from dataclasses import dataclass
from scipy.ndimage import binary_fill_holes, correlate, generate_binary_structure


def display_blizzards(blizzards):
    symbols = '><v^'
    out = []
    for ix in range(blizzards[0].shape[0]):
        out.append("\n")
        for jx in range(blizzards[0].shape[1]):
            c = "."
            for bix in range(4):
                if blizzards[bix][ix][jx]:
                    if c == ".":
                        c = symbols[bix]
                    elif c in symbols:
                        c = "2"
                    else:
                        c = str(int(c) + 1)
            out.append(c)
    print("".join(out))


def day24(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(line.strip())

    # Enough of a border that in 10 rounds we won't hit it:w


    blizzards = []
    for blizzard in '><v^':
        field = np.zeros(shape=(len(data)-2, len(data[0])-2), dtype=bool)
        blizzards.append(field)

        for ix, line in enumerate(data[1:-1]):
            for jx, lc in enumerate(line[1:-1]):
                if lc == blizzard:
                    field[ix, jx] = 1


    positions = {(-1, 0)}

    for ronde in itertools.count():
        for ix in range(4):
            if ix == 0:
                blizzards[ix] = np.roll(blizzards[ix], 1, axis=1)
            elif ix == 1:
                blizzards[ix] = np.roll(blizzards[ix], -1, axis=1)
            elif ix == 2:
                blizzards[ix] = np.roll(blizzards[ix], 1, axis=0)
            elif ix == 3:
                blizzards[ix] = np.roll(blizzards[ix], -1, axis=0)

        break

    display_blizzards(blizzards)


    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day24(examples("24"))
day24(inputs("24"))
