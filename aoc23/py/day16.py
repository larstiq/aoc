#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs, display_dfield

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


    heads = [(0, -1)]
    directions = [(0, 1)]
    seen = set()

    energized = pd.DataFrame(data=np.nan, index=df.index, columns=df.columns)

    #energized[heads[0][1]][heads[0][0]] = '#'

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

        seen |= nextseen 
        for (h, d) in notseen:
            advance = h[0] + d[0], h[1] + d[1]
            if advance[0] in df.index and advance[1] in df.columns:
                row, col = advance
                char = df[col][row]
                energized[col][row] = '#'

                if char == '.':
                    heads.append(advance)
                    directions.append(d)
                elif char == '|':
                    if d in ((0, -1), (0, 1)):
                        heads.append(advance)
                        heads.append(advance)
                        directions.extend([(1, 0), (-1, 0)])
                    else:
                        heads.append(advance)
                        directions.append(d)
                elif char == '-':
                    if d in ((-1, 0), (1, 0)):
                        heads.append(advance)
                        heads.append(advance)
                        directions.extend([(0, -1), (0, 1)])
                    else:
                        heads.append(advance)
                        directions.append(d)
                elif char == '/':
                    if d == (-1, 0):
                        heads.append(advance)
                        directions.append((0, 1))
                    elif d == (1, 0):
                        heads.append(advance)
                        directions.append((0, -1))
                    elif d == (0, -1):
                        heads.append(advance)
                        directions.append((1, 0))
                    elif d == (0, 1):
                        heads.append(advance)
                        directions.append((-1, 0))
                elif char == '\\':
                    if d == (-1, 0):
                        heads.append(advance)
                        directions.append((0, -1))
                    elif d == (1, 0):
                        heads.append(advance)
                        directions.append((0, 1))
                    elif d == (0, -1):
                        heads.append(advance)
                        directions.append((-1, 0))
                    elif d == (0, 1):
                        heads.append(advance)
                        directions.append((1, 0))


    print(energized)
    part1 =  (energized == '#').sum().sum()
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day16(examples("16"))
day16(inputs("16"))
