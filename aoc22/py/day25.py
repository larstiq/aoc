#!/usr/bin/env python

import itertools
from collections import Counter, defaultdict, deque

from utils import examples, inputs

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
    return sum(c * 5 ** ix for ix, c in enumerate(snafu_list))


def largest_five_place(number):
    for ix in itertools.count():
        if 5 ** ix >= number:
            return ix


def snafu_to_decimal(snafu):
    return list_to_decimal(snafu_to_list(snafu))


def in_snafu_range(number, coeff, remaining_digits):
    first_digit = decimal2snafu[coeff]
    lower = first_digit + "=" * remaining_digits
    upper = first_digit + "2" * remaining_digits

    return snafu_to_decimal(lower) <= number <= snafu_to_decimal(upper)


def decimal_to_list(number):
    ix = largest_five_place(number)
    remainder = number
    five_places = {jx: 0 for jx in range(ix)}

    while ix > 0:
        for coeff in [1, 2, -2, -1]:
            if in_snafu_range(remainder, coeff, ix):
                five_places[ix] = coeff
                remainder -= coeff * 5 ** ix
                break

        ix -= 1

    five_places[0] = remainder

    return [v for (k, v) in sorted(five_places.items())]


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
    lists_again = [decimal_to_list(d) for d in as_decimals]
    print("decimals to lists", lists_again, snafus_as_lists == lists_again)
    snafus_again = [list_to_snafu(l) for l in lists_again]
    print("snafus again", snafus_again, snafus == snafus_again)

    total_decimal = sum(as_decimals)
    print("total decimal", total_decimal)
    print(decimal_to_list(total_decimal))
    part1 = list_to_snafu(decimal_to_list(total_decimal))

    print("part1:", part1)
    print("part2:", "start the blender")
    breakpoint()


day24(examples("25"))
day24(inputs("25"))
