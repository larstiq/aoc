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

    for ronde in itertools.count(1):
        next_positions = set()
        for ix in range(4):
            if ix == 0:
                blizzards[ix] = np.roll(blizzards[ix], 1, axis=1)
            elif ix == 1:
                blizzards[ix] = np.roll(blizzards[ix], -1, axis=1)
            elif ix == 2:
                blizzards[ix] = np.roll(blizzards[ix], 1, axis=0)
            elif ix == 3:
                blizzards[ix] = np.roll(blizzards[ix], -1, axis=0)

        # TODO: consider combined blizzards and positions map, 1-connected + center

        for pos in positions:
            for (dx, dy) in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                step = pos[0] + dx, pos[1] + dy
                if step[0] == blizzards[0].shape[0] and step[1] == blizzards[0].shape[1] - 1:
                    breakpoint()
                    print("Found the exit point")

                elif step[0] == -1 and step[1] == 0:
                    next_positions.add((-1, 0))
                    print("Back at start")

                elif step[0] < 0 or step[1] < 0 or step[0] >= blizzards[0].shape[0] or step[1] >= blizzards[0].shape[1]:
                    # Can't step onto a wall, skip it
                    continue

                for blizzard in blizzards:
                    if blizzard[step[0], step[1]]:
                        break
                else:
                    next_positions.add((step[0], step[1]))

        print(f"Ending round {ronde} with {len(next_positions)} positions")
        print(next_positions)
        display_blizzards(blizzards)
        print('-' * 80)
        positions = next_positions

        if ronde == 1:
            assert (0, 0) in positions
        elif ronde == 2:
            assert (1, 0) in positions
        elif ronde == 3:
            assert (1, 0) in positions
        elif ronde == 4:
            assert (0, 0) in positions
        elif ronde == 5:
            assert (0, 1) in positions
        elif ronde == 6:
            assert (0, 2) in positions
        elif ronde == 7:
            assert (1, 2) in positions
        elif ronde == 8:
            assert (1, 1) in positions
        elif ronde == 9:
            assert (0, 1) in positions
        elif ronde == 10:
            assert (0, 2) in positions
        elif ronde == 11:
            assert (0, 2) in positions
        elif ronde == 12:
            assert (1, 2) in positions
        elif ronde == 13:
            assert (2, 2) in positions
        elif ronde == 14:
            assert (2, 3) in positions
        elif ronde == 15:
            assert (2, 4) in positions
        elif ronde == 16:
            assert (2, 5) in positions
        elif ronde == 10:
            assert (3, 5) in positions
        elif ronde == 10:
            assert (4, 5) in positions

        if ronde > 20:
            break





    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day24(examples("24"))
day24(inputs("24"))
