#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools


def sign(number):
    if number == 0:
        return number
    return int(math.copysign(1, number))


def compare_packets(left, right):
    if isinstance(left, list) and isinstance(right, list):
        for (l, r) in zip(left, right):
            res = compare_packets(l, r)
            if res != 0:
                return res
        return sign(len(left) - len(right))
    elif isinstance(left, int) and isinstance(right, int):
        return sign(left - right)
    elif isinstance(left, int) and isinstance(right, list):
        return compare_packets([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare_packets(left, [right])


def day13(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        packets = [json.loads(line) for line in puzzlein if line.strip() != ""]

    right_order_sum = 0
    for ix, (left, right) in enumerate(more_itertools.chunked(packets, 2)):
        if compare_packets(left, right) == -1:
            right_order_sum += 1 + ix
        logging.debug("index: %s left: %s right: %s", ix, left, right)

    print("part1:", right_order_sum)

    dividers = [[[2]], [[6]]]
    divided_packets = packets + dividers
    divided_packets.sort(key=functools.cmp_to_key(compare_packets))

    decoder = math.prod(map(lambda d: divided_packets.index(d) + 1, dividers))
    print("part2:", decoder)


logging.getLogger().setLevel(logging.WARN)

day13(examples("13"))
day13(inputs("13"))
