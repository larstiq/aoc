#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs, display_dfield

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math
import functools
import operator


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
    

    def roll_faster(df):
        nextdf = df.copy()
        for col in df.columns:
            nextdf[col] = functools.reduce(operator.add, [list(sorted(group, reverse=True)) for key, group in itertools.groupby(df[col], lambda x: x == '#')])
        return pd.DataFrame(nextdf)

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
    first = True
    breakpoint()
    for cycle in range(1000000000):
        print("Cycle", cycle)

        if nextdfkey is not None:
            prevkey = nextdfkey
        else:
            if first:
                prevdf = df.copy()
                first = False
            else:
                prevdf = nextdf.copy()

            prevkey = tuple(tuple(r) for r in prevdf.values)

        if prevkey not in cache:
            #nextdf = roll(nextdf, [-1, 0])
            nextdf = roll_faster(prevdf)
            #old_north = roll(pd.DataFrame(prevdf), [-1, 0])
            if False and not old_north.equals(nextdf):
                breakpoint()
            #display_dfield(nextdf)
            #nextdf = roll(nextdf, [0, -1])
            rotated = pd.DataFrame(np.rot90(nextdf, k=3))
            #old_west = roll(pd.DataFrame(nextdf), [0, -1])
            nextdf = pd.DataFrame(np.rot90(roll_faster(rotated)))
            if False and not old_west.equals(pd.DataFrame(nextdf)):
                breakpoint()
            #display_dfield(nextdf)
            #nextdf = roll(nextdf, [1, 0])
            rotated = pd.DataFrame(np.rot90(nextdf, k=2))
            #old_south = roll(pd.DataFrame(nextdf), [+1, 0])
            nextdf = pd.DataFrame(np.rot90(roll_faster(rotated), k=2))
            if False and not old_south.equals(pd.DataFrame(nextdf)):
                breakpoint()
            #display_dfield(nextdf)
            #nextdf = roll(nextdf, [0, 1])
            rotated = pd.DataFrame(np.rot90(nextdf, k=1))
            #old_east = roll(pd.DataFrame(nextdf), [0, 1])
            nextdf = pd.DataFrame(np.rot90(roll_faster(rotated), k=3))
            if False and not old_east.equals(pd.DataFrame(nextdf)):
                breakpoint()
            #display_dfield(nextdf)
            #print(cycle, sum([(df.shape[0] - ix) * count for ix, count in enumerate((nextdf == 'O').sum(axis=1))]))
            cache[prevkey] = tuple(tuple(r) for r in nextdf.values)
            cyclemap[prevkey].append(cycle)
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
