#!/usr/bin/env python

from utils import inputs, examples

import collections
import copy
import logging
import math

import sympy

import pandas as pd

import numpy as np
import string
import networkx
import itertools


def cmp_nested_list(left, right):
    for (l, r) in zip(left, right):
        if isinstance(l, int) and isinstance(r, int):
            if l == r:
                continue
            if l < r:
                return -1
            else:
                return 1
        elif isinstance(l, list) and isinstance(r, list):
            res = cmp_nested_list(l, r)
            if res == 0:
                continue
            return res
        elif isinstance(l, int) and isinstance(r, list):
            return cmp_nested_list([l], r)
        elif isinstance(l, list) and isinstance(r, int):
            return cmp_nested_list(l, [r])

    # All items compare equal, are lists same length?
    if len(left) == len(right):
        return 0

    if len(left) < len(right):
        return -1
    else:
        return 1



def day13(filename):
    print()
    print(filename)

    packet_pairs = []
    all_packets = []
    with open(filename) as puzzlein:
        packets = puzzlein.read()

        for pair in packets.split("\n\n"):
            packet_pairs.append(tuple(map(eval, pair.strip().split("\n"))))
            all_packets.extend(packet_pairs[-1])


    right_order_sum = 0
    for ix, (left, right) in enumerate(packet_pairs):
        if cmp_nested_list(left, right) == -1:
            right_order_sum += 1 + ix
        print(ix, left, right)

    print("part1:", right_order_sum)


    import functools
    dividers = [[[2]], [[6]]]
    all_packets_plus_diviers = all_packets + dividers
    all_packets_plus_diviers.sort(key=functools.cmp_to_key(cmp_nested_list))


    print("part2:", (all_packets_plus_diviers.index(dividers[0]) + 1) * (1 + all_packets_plus_diviers.index(dividers[1])))






logging.getLogger().setLevel(logging.DEBUG)

day13(examples("13"))
day13(inputs("13"))
