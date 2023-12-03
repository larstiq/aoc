#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools

import string

def day03(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    symbols = set()
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            symbols.update(line)
            data.append(list(line))

    df = pd.DataFrame(data)
    real_symbols = symbols - set(string.digits) - set(".")

    symbol_pos = df.isin(real_symbols)

    for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        for pos in df[df.isin(real_symbols)].stack().index:
            try:
                ding = df[pos[0] + direction[0]][pos[1] + direction[1]] 
            except:
                break

            if ding in(string.digits):
                for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    for i in itertools.count():
                        try:
                            dong = df[pos[0] + direction[0] + i*dx][pos[1] + direction[1] + i*dy]
                        except:
                            pass
                            in (string.digits):
                    while 

                    print(pos[0] + direction[0] + i*dx,pos[1] + direction[1] + i*dy)
                    print(pos[0] + direction[0] + 0*dx,pos[1] + direction[1] + 0*dy)


    print(df)
    breakpoint()
    print("part1:", part1)
    print("part2:", part2)


day03(examples("03"))
#day03(inputs("03"))
