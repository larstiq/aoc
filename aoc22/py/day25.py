#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict, deque, Counter
import time

import numpy as np
import re
import itertools

import networkx as nx
import sympy

from dataclasses import dataclass
from scipy.ndimage import binary_fill_holes, correlate, generate_binary_structure


snafu2decimal = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
decimal2snafu = {v: k for (k, v) in snafu2decimal.items()}


def snafu_to_list(snafu):
    coefficients = []
    for c in reversed(snafu):
        coefficients.append(snafu2decimal[c])

    return coefficients

def list_to_decimal(snafu_list):
    return sum(c * 5**ix for ix, c in enumerate(snafu_list))


def largest_five_place(number):
    for ix in itertools.count():
        if 5**ix >= number:
            return ix


def snafu_to_decimal(snafu):
    return list_to_decimal(snafu_to_list(snafu))


def peal(number):
    if number == 497:
        breakpoint()
    # TODO: zero?
    for ix in itertools.count():
        if 5**ix >= number:
            if 5**ix <= number:
                return {ix: 1}, number - 5**ix
            elif 5**ix - 5**(ix - 1) <= number:
                return {ix: 1, ix - 1: -1}, number - (5**ix - 5**(ix - 1))
            elif 5**ix - 2*5**(ix - 1) <= number:
                return {ix: 1, ix - 1: - 2}, number - (5**ix - 2*5**(ix - 1))
            elif 2*5**(ix - 1) <= number:
                return {ix - 1: 2}, number - 2*5**(ix - 1)
            elif 1*5**(ix - 1) <= number:
                return {ix - 1: 1}, number - 1*5**(ix - 1)
            else:
                return {ix - 1: 0}, number


def decimal_to_list(number):
    ix = largest_five_place(number)
    remainder = number
    five_places = {jx: 0 for jx in range(ix)}

    while remainder != 0:
        #lower = snafu_to_decimal("1" + "=" * ix)
        #upper = snafu_to_decimal("1" + "0" * ix)

        #assert lower <= remainder <= upper

        # The leading two digits can be either
        # "10" (exact match), "1-" or "1="

        if number == 906:
            pass

        if ix < 0 and remainder < 3:
            breakpoint()
            five_places[0] = 1


        if   snafu_to_decimal("1=" + "=" * (ix - 1)) <= remainder <= snafu_to_decimal("1" + "2" * ix):
            five_places[ix] = 1
            remainder -= 5**ix
            ix -= 1
        elif snafu_to_decimal("2=" + "=" * (ix - 1)) <= remainder <= snafu_to_decimal("2" + "2" * ix):
            five_places[ix] = 2
            remainder -= 2*5**ix
            ix -= 1
        elif snafu_to_decimal("==" + "=" * (ix - 1)) <= remainder <= snafu_to_decimal("=" + "2" * ix):
            five_places[ix] = -2
            remainder -= -2*5**ix
            ix -= 1
        elif snafu_to_decimal("-=" + "=" * (ix - 1)) <= remainder <= snafu_to_decimal("-" + "2" * ix):
            five_places[ix] = -1
            remainder -= -1*5**ix
            ix -= 1
        else:
            if ix > max(five_places):
                pass
            elif ix > 0:
                five_places[ix] = 0
            else:
                assert 0 <= remainder < 3
                assert ix == 0
                five_places[0] = remainder
                remainder = 0

            ix -= 1

    assert remainder == 0

    res = [v for (k, v) in sorted(five_places.items())]
    if res[-1] == 0:
        breakpoint()
    return res

def list_to_snafu(lijst):
    return "".join(decimal2snafu[d] for d in reversed(lijst))


def day24(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    snafus = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            snafus.append(line.strip())

    print("snafus", snafus)
    snafus_as_lists = [snafu_to_list(snafu) for snafu in snafus]
    print("as lists", snafus_as_lists)
    as_decimals = [list_to_decimal(l) for l in snafus_as_lists]
    print("as decimals", as_decimals)
    print("decimals to lists", [decimal_to_list(d) for d in as_decimals])
    print("snafus", [list_to_snafu(decimal_to_list(d)) for d in as_decimals])

    total_decimal = sum(as_decimals)
    print(total_decimal)
    print(decimal_to_list(total_decimal))
    part1 = list_to_snafu(decimal_to_list(total_decimal))

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day24(examples("25"))
day24(inputs("25"))
