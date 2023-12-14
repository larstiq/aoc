#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math


def day14(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(list(line.strip()))

    df = pd.DataFrame(data)
    orig = df.copy()
    


    def roll(df, direction):
        prev = pd.DataFrame(data=np.zeros(df.shape))
        nextdf = df.copy()

        while not prev.equals(nextdf):
            prev = nextdf.copy()
            for row in df.index:
                if row == 0:
                    continue
                for col in df.columns:
                    besides = prev[col + direction[1]][row + direction[0]]
                    if prev[col][row] == 'O' and besides == '.':
                        nextdf[col + direction[1]][row + direction[0]] = 'O'
                        nextdf[col][row] = '.'
        return nextdf


    nextdf = roll(df, [-1, 0])

    load = [(df.shape[0] - ix) * count for ix, count in enumerate((nextdf == 'O').sum(axis=1))]

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day14(examples("14"))
day14(inputs("14"))
