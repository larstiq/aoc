#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools

import string



def display_blizzards(blizzards):
    symbols = '><v^'
    out = []
    for ix in range(blizzards.shape[0]):
        out.append("\n")
        for jx in range(blizzards.shape[1]):
           if isinstance(blizzards[jx][ix], float):
              c = " "
           else:
              c = blizzards[jx][ix]
           out.append(c)
    print("".join(out))

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

    import scipy


    maybe_partts = df.isin(set(string.digits))

    structure = scipy.ndimage.generate_binary_structure(2, 2)

    neighbours = scipy.ndimage.binary_dilation(symbol_pos, structure) & maybe_partts
    prev = maybe_partts
    nextn = scipy.ndimage.binary_dilation(symbol_pos, structure) & maybe_partts
    leftright = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
    while not prev.equals(nextn):
        prev = nextn
        nextn = scipy.ndimage.binary_dilation(nextn, leftright) & maybe_partts


    breakpoint()
    parts = []
    for ix, row in df[nextn].iterrows():
        accum = []
        for char in row:
            if isinstance(char, float):
                if accum != []:
                    parts.append(int(''.join(accum)))
                    accum = []
            elif char in string.digits:
                accum.append(char)
            else:
                print("Error!")
                breakpoint()

    breakpoint()

    print(df)
    part1 = sum(parts)
    print("part1:", part1)
    print("part2:", part2)


day03(examples("03"))
day03(inputs("03"))
