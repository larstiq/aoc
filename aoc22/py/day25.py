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
    five_places = {}
    
    while ix > -1:
        if ix in five_places:
            breakpoint()
            ix -= 1
            continue
        if 5**ix >= remainder:
            if 5**ix <= remainder:
                five_places[ix] = 1
                remainder -= 5**ix
            elif 5**ix - 5**(ix - 1) <= remainder:
                five_places[ix] = 1
                five_places[ix - 1] = -1
                remainder -= 5**ix - 5**(ix - 1)
            # This doens't work because in case of 1== we still need to pick 1= here.
            elif 5**ix - 2*5**(ix - 1) <= remainder:
                five_places[ix] = 1
                five_places[ix - 1] = -2
                remainder -= 5**ix - 2*5**(ix - 1)
        elif 2*5**ix <= remainder:
            breakpoint()
            five_places[ix] = 2
            remainder -= 2*5**ix
        else:
            five_places[ix] = 0

        if number - remainder != sum(v*5**k for (k, v) in five_places.items()):
            breakpoint()

        ix -= 1

    return [v for (k, v) in sorted(five_places.items())]


def list_to_snafu(lijst):
    return "".join(decimal2snafu[d] for d in reversed(lijst))


def day24(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(snafu_to_list(line.strip()))

    print(data)

    as_decimals = [list_to_decimal(l) for l in data]
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
