#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs, display_field

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math


def day16(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(list(line.strip()))

    df = pd.DataFrame(data)
    # Rows grow down, orient with complex plane
    field = np.array([row for row in reversed(data)])

    def energize(heads, directions):

        seen = set()
        energized = np.zeros_like(field, dtype=str)

        UP, DOWN, LEFT, RIGHT = 1j, -1j, -1, 1

        while True:
            nexthd = set(list(zip(heads, directions)))
            heads = []
            directions = []

            nextseen = set(nexthd)
            if nextseen.issubset(seen):
                break

            notseen = nextseen - seen
            if len(notseen) < len(nextseen):
                #breakpoint()
                pass

            display_field(field)
            display_field(energized)
            
            seen |= nextseen 
            #breakpoint()
            for (h, d) in notseen:
                advance = h[0] + int(d.real), h[1] + int(d.imag)
                print(f"From {h} by {d} gets to {advance}")
                #breakpoint()
                if 0 <= advance[0] < field.shape[1] and 0 <= advance[1] < field.shape[0]:
                    x, y = advance
                    char = field[x, y]
                    energized[x, y] = '#'

                    if char == '.':
                        heads.append(advance)
                        directions.append(d)
                    elif char == '|': # up/left continue, left/right split
                        if d.real == 0:
                            heads.append(advance)
                            directions.append(d)
                        else:
                            heads.append(advance)
                            heads.append(advance)
                            directions.extend([-1j, 1j])
                    elif char == '-':  # up/left split, left/right continue
                        if d.real == 0:
                            heads.append(advance)
                            heads.append(advance)
                            directions.extend([-1, -1])
                        else:
                            heads.append(advance)
                            directions.append(d)
                    elif char == '/':
                        heads.append(advance)
                        if d.real == 0:
                            directions.append(d*-1j)
                        else:
                            directions.append(d*1j)
                    elif char == '\\':
                        heads.append(advance)
                        if d.real == 0:
                            directions.append(d*1j)
                        else:
                            directions.append(d*-1j)

        return energized, (energized == 1).sum().sum()


    energize_counts = []

    for pos in range(field.shape[0]):
        print("Horizontal", pos)
        print("...from the left")
        heads = [(-1, pos)]
        directions = [1]
        energize_counts.append(energize(heads, directions)[1])
        if heads[0] == (-1, 0):
            part1 = energize_counts[-1]

        breakpoint()

        print("...from the right")
        heads = [(field.shape[0], pos)]
        directions = [-1]
        energize_counts.append(energize(heads, directions)[1])

    for pos in range(field.shape[1]):
        print("Vertical", pos)
        print("...from below", pos)
        heads = [(pos, -1)]
        directions = [1j]
        energize_counts.append(energize(heads, directions)[1])

        print("...from above", pos)
        heads = [(pos, field.shape[1])]
        directions = [-1j]
        energize_counts.append(energize(heads, directions)[1])

    part2 = max(energize_counts)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day16(examples("16"))
day16(inputs("16"))
