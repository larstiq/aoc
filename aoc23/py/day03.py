#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools

import string
import scipy

from scipy.ndimage import generate_binary_structure, binary_dilation, binary_propagation, label

digits = set(string.digits)


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

    real_symbols = symbols - digits - set(".")

    symbol_pos = df.isin(real_symbols)
    maybe_partts = df.isin(digits)
    structure = generate_binary_structure(2, 2)
    leftright = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])

    neighbours = binary_dilation(symbol_pos, structure) & maybe_partts
    nextn = binary_propagation(neighbours, leftright, mask=maybe_partts) & maybe_partts
    breakpoint()

    lelijk = [int(x) for x in ''.join(''.join(row) for row in df[nextn].fillna(" ").values).split(" ") if x != '']
    part1 = sum(lelijk)
    
    gears = df.isin(set('*'))
    gear_ratios = []

    for gear_pos in df[gears].stack().index:
        block = df[gear_pos[0] -1:gear_pos[0] + 2][[gear_pos[1] - 1, gear_pos[1], gear_pos[1] + 1]]
        labels, nb = label(block.isin(digits))
        if nb > 1:
            real_gear_pos = (df == 0)
            real_gear_pos[gear_pos[1]][gear_pos[0]] = True
            neighbours = binary_dilation(real_gear_pos, structure) & maybe_partts
            nextn = binary_propagation(neighbours, leftright, mask=maybe_partts) & maybe_partts
            lelijk = [int(x) for x in ''.join(''.join(row) for row in df[nextn].fillna(" ").values).split(" ") if x != '']
            gear_ratios.append(math.prod(lelijk))


    part2 = sum(gear_ratios)

    if str(filename).endswith("inputs/01"):
        assert part1 == 533775
        assert part2 == 78236071
    print("part1:", part1)
    print("part2:", part2)


day03(examples("03"))
day03(inputs("03"))
