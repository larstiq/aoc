#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs, display_dfield

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math


def day13(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    dfs = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            if line == "\n":
                dfs.append(pd.DataFrame(data))
                data = []
            else:
                data.append(list(line.strip()))


    dfs.append(pd.DataFrame(data))
    print(dfs)

    def countups(df):
        ups = []
        row_reflections = (df == df.shift(axis=0)).sum(axis=1) == df.shape[1]

        for ix, row in enumerate(row_reflections):
            if row == False:
                continue

            shortest = min(ix, len(row_reflections) - ix)
            upref = df.loc[ix - shortest:ix - 1]
            downref = df.loc[ix:ix + shortest - 1]
            equal = upref.values == downref[::-1].values
            if equal.all():
                ups.append(ix)


        #if (df.iloc[-1] == df.iloc[-2]).sum() == df.shape[1]:
        #    breakpoint()

        #if (df.iloc[0] == df.iloc[1]).sum() == df.shape[1]:
        #    breakpoint()

        display_dfield(df)
        print(ups)
        #if ups == [3]:
        #    breakpoint()
        return sum(ups)


    dingen = []
    for df in dfs:
        dingen.append(countups(df.T) + 100 * countups(df))
        #counted = len(x == df.shape[1] for x in equal.sum(axis=1))


        
    print(dingen)
    part1 = sum(dingen)
    print("part1:", part1)
    print("part2:", part2)

    # If there is a reflection then we must have two adjacent rows/columns being the same, let's start ther
    breakpoint()



day13(examples("13"))
day13(inputs("13"))
