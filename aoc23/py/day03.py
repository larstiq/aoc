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

from scipy.ndimage import (
    generate_binary_structure,
    binary_dilation,
    binary_propagation,
    label,
)

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

    maybe_parts = df.isin(digits)
    friends = generate_binary_structure(2, 2)
    leftright = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])

    digits_bordering_symbols = (
        binary_dilation(df.isin(real_symbols), friends) & maybe_parts
    )
    parts_bordering_symbols = df.where(
        binary_propagation(digits_bordering_symbols, leftright, mask=maybe_parts)
    )
    # Part numbers are separated by nans. Turn into one string with numbers separated by whitespace
    aap = ''.join(parts_bordering_symbols.fillna(' ').values.reshape(1, df.size).tolist()[0])
    # Split the number string and make real ints
    part_numbers = [int(number) for number in aap.split()]

    part1 = sum(part_numbers)


    gears = df == "*"
    gear_ratios = []
    breakpoint()

    for gear_pos in df[gears].stack().index:
        block = df[gear_pos[0] - 1 : gear_pos[0] + 2][
            [gear_pos[1] - 1, gear_pos[1], gear_pos[1] + 1]
        ]
        labels, nb = label(block.isin(digits))
        if nb > 1:
            real_gear_pos = df == 0
            real_gear_pos[gear_pos[1]][gear_pos[0]] = True
            # breakpoint()
            digits_bordering_gears = (
                binary_dilation(real_gear_pos, friends) & maybe_parts
            )
            parts_bordering_gears = df.where(
                binary_propagation(digits_bordering_gears, leftright, mask=maybe_parts)
            )
            # Part numbers are separated by nans. Turn into one string with numbers separated by whitespace
            hond = ''.join(parts_bordering_gears.fillna(' ').values.reshape(1, df.size).tolist()[0])
            # Split the number string and make real ints
            part_numbers = [int(number) for number in hond.split()]
            gear_ratios.append(math.prod(part_numbers))

    part2 = sum(gear_ratios)

    if str(filename).endswith("inputs/01"):
        assert part1 == 533775
        assert part2 == 78236071
    print("part1:", part1)
    print("part2:", part2)


day03(examples("03"))
day03(inputs("03"))
