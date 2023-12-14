#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs, display_dfield

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
            # TODO: could also just rotate the field

            if direction[0] >= 0:
                roworder = df.index
            else:
                roworder = df.index[::-1]

            if direction[1] >= 0:
                colorder = df.columns
            else:
                colorder = df.columns[::-1]

            for row in roworder:
                if not (0 <= row + direction[0] < df.shape[0]):
                    #print("Not row", row + direction[0])
                    continue
                for col in colorder:
                    if not ( (0 <= col + direction[1] < df.shape[1])):
                        #print("Not col", col + direction[1])
                        continue
                    besides = prev[col + direction[1]][row + direction[0]]
                    if prev[col][row] == 'O' and besides == '.':
                        nextdf[col + direction[1]][row + direction[0]] = 'O'
                        nextdf[col][row] = '.'
        return nextdf


    nextdf = df.copy()
    #for cycle in range(3):
    cache = {}
    cyclemap = defaultdict(list)
    nextdfkey = None
    for cycle in range(1000000000):
        print("Cycle", cycle)

        if nextdfkey is not None:
            prevkey = nextdfkey
        else:
            prevdf = nextdf.copy()
            prevkey = tuple(tuple(r) for r in prevdf.values)

        if prevkey not in cache:
            print("...Rolling")
            nextdf = roll(nextdf, [-1, 0])
            #display_dfield(nextdf)
            nextdf = roll(nextdf, [0, -1])
            #display_dfield(nextdf)
            nextdf = roll(nextdf, [1, 0])
            #display_dfield(nextdf)
            nextdf = roll(nextdf, [0, 1])
            #display_dfield(nextdf)
            #print(cycle, sum([(df.shape[0] - ix) * count for ix, count in enumerate((nextdf == 'O').sum(axis=1))]))
            print("...Done rolling")
            print("...adding to cache")
            cache[prevkey] = tuple(tuple(r) for r in nextdf.values)
            cyclemap[prevkey].append(cycle)
            print("...added")
        else:
            cyclemap[prevkey].append(cycle)
            break

    for (key, value) in cyclemap.items():
        if len(value) == 2:
            start = key
            cyclelength = value[1] - value[0]
            # We enter the cycle at the first occurrence, the remaining steps
            # we mod by the cycle length and then we can go back to the map
            reduced = (1000000000 - 1 - value[0]) % cyclelength 
            find = [1 + value[0] + reduced]
            break

    for (key, value) in cyclemap.items():
        if value == find:
            nextdf =  pd.DataFrame(data=key)
            break

    def load(nextdf):
        load = [(df.shape[0] - ix) * count for ix, count in enumerate((nextdf == 'O').sum(axis=1))]
        return load

    part1 = sum(load(nextdf))

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day14(examples("14"))
day14(inputs("14"))
