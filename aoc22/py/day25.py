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
    remainder = number
    five_places = {}
    while remainder > 0:
        next_coefficients, next_remainder = peal(remainder)
        five_places.update(next_coefficients)
        if number - next_remainder != sum(v*5**k for (k, v) in five_places.items()):
            breakpoint()
        remainder = next_remainder

    return [v for (k, v) in sorted(five_places.items())]


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
    print(as_decimals)
    print([decimal_to_list(d) for d in as_decimals])

    total_decimal = sum(as_decimals)
    print(total_decimal)

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day24(examples("25"))
day24(inputs("25"))
