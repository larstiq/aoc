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

        def reflect(df, breakp=False):
            ups = []
            row_reflections = (df == df.shift(axis=0)).sum(axis=1) == df.shape[1]

            if breakp:
                breakpoint()

            # Two adjacent rows are the same, might they extend to a perfect reflection?
            reflection_indices = row_reflections[row_reflections].index

            #if len(reflection_indices) > 1:
            #    breakpoint()
            for ix in reflection_indices:
                shortest = min(ix, len(row_reflections) - ix)

                upref = df.loc[ix - shortest:ix - 1]
                downref = df.loc[ix:ix + shortest - 1]

                assert upref.shape == downref.shape
                equal = upref.values == downref[::-1].values
                if equal.all():
                    #breakpoint()
                    #print(ix, row_reflections, upref.shape, downref.shape, df.shape)
                    ups.append(ix)


            return ups

        def smudge(df, pos):
            row, col = pos
            smudged = df.copy()
            smudged[col][row] = '#' if df[col][row] == '.' else '.'
            return smudged

        ups = reflect(df)

        # Now with smudges
        smudged_refs = {}
        new_reflections = set([])
        for refs in smudged_refs.values():
            new_reflections |= set(refs)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                newups = reflect(smudge(df, (row, col)))
                if len(newups) > 0 and newups != ups:
                    smudged_refs[(row, col)] = tuple(newups)
                    new_reflections |= set(newups)
                    diff = new_reflections - set(ups)
                    if len(diff) == 0:
                        continue
                    elif len(diff) == 1:
                        return list(diff)[0]


        #if len(smudged_refs.keys()) > 1:
        #    print(ups, smudged_refs)
        #    #breakpoint()
        #    print("wat")
        return 0


        diff = new_reflections - set(ups)
        if len(diff) == 0:
            return 0
        elif len(diff) == 1:
            return list(diff)[0]
        else:
            print("wat")
            breakpoint()
            print("wat")
        #return sum(sum(r) for r in smudged_refs.values() if r not in ups)
        return new_reflection

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
