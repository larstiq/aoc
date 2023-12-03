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
    binary_propagation as propagation,
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
    parts_bordering_symbols = propagation(
        digits_bordering_symbols, leftright, mask=maybe_parts
    )
    # Part numbers are separated by nans. Turn into one string with numbers separated by whitespace
    parts_bordering_symbols_padded = (
        df[maybe_parts]
        .fillna(" ")
        .where(binary_dilation(parts_bordering_symbols, leftright))
    )
    number_string = "".join(parts_bordering_symbols_padded.stack())
    # Split the number string and make real ints
    part_numbers = [int(number) for number in number_string.split()]
    part1 = sum(part_numbers)

    # Label each connected component containing a gear
    gears = df == "*"
    gear_regions, nregions = label(
        propagation(gears, friends, mask=maybe_parts), friends
    )
    labels = np.arange(1, nregions + 1)

    def gear_ratios_in_region(gear_region, positions):
        emit = []
        accum = []
        prevpos = None
        # labeled_comprehension may (and WILL) give the values of the digit
        # cells bordering on a gear in a non-linear order. That's fine when
        # you're using np.mean but for us the order of the digits actually
        # matters.
        #
        # Sort by the (linear) position in the numpy array. Legitimate engine
        # part numbers will then be a sequence of positions increasing by
        # exactly 1.
        for pos, val in sorted(zip(positions, gear_region)):
            if val == "*":
                continue
            if accum == [] or pos == prevpos + 1:
                accum.append(val)
            elif pos > prevpos + 1:
                emit.append(int("".join(accum)))
                accum = [val]

            prevpos = pos

        emit.append(int("".join(accum)))
        if len(emit) > 1:
            ratio = math.prod(emit)
        else:
            ratio = 0
        return ratio

    gear_ratios = scipy.ndimage.labeled_comprehension(
        df, gear_regions, labels, gear_ratios_in_region, int, 0, pass_positions=True
    )

    part2 = sum(gear_ratios)

    if str(filename).endswith("inputs/01"):
        assert part1 == 533775
        assert part2 == 78236071
    print("part1:", part1)
    print("part2:", part2)


day03(examples("03"))
day03(inputs("03"))
