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

    found = False
    snack = None
    foundagain = False
    for ronde in itertools.count(1):
        if foundagain:
            breakpoint()
            break

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


        # TODO: extract start and end positions to compute once

        for pos in positions:
            for (dx, dy) in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                step = pos[0] + dx, pos[1] + dy
                if ronde == 42:
                    print(step)
                if step[0] == blizzards[0].shape[0] and step[1] == blizzards[0].shape[1] - 1:
                    if not found:
                        found = True
                        part1 = ronde
                        next_positions.clear()
                        next_positions.add(step)
                        break
                    elif snack is not None:
                        foundagain = True
                        part2 = ronde
                        next_positions.clear()
                        next_positions.add(step)
                        break
                    else: # Temporary shelter
                        next_positions.add(step)
                        continue

                elif step[0] == -1 and step[1] == 0:
                    if found and snack is None:
                        snack = ronde
                        next_positions.clear()
                        next_positions.add(step)
                        breakpoint()
                        break
                    else:
                        next_positions.add(step)
                        continue


                elif step[0] < 0 or step[1] < 0 or step[0] >= blizzards[0].shape[0] or step[1] >= blizzards[0].shape[1]:
                    # Can't step onto a wall, skip it
                    continue

                for blizzard in blizzards:
                    if blizzard[step[0], step[1]]:
                        break
                else:
                    next_positions.add(step)

            if found and ronde == part1:
                break
            if snack == ronde:
                break

        if len(next_positions) == 0:
            breakpoint()

        print(f"Ending round {ronde} with {len(next_positions)} positions")
        print(next_positions)
        display_blizzards(blizzards)
        print('-' * 80)
        positions = next_positions


    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day24(examples("24"))
day24(inputs("24"))
