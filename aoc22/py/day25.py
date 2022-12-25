#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

snafu2decimal = dict(zip("210-=", range(2, -3, -1)))
decimal2snafu = {v: k for (k, v) in snafu2decimal.items()}


def snafu_to_decimal(snafu):
    coefficients = []
    for c in reversed(snafu):
        coefficients.append(snafu2decimal[c])

    return sum(c * 5**ix for ix, c in enumerate(coefficients))


def in_snafu_range(number, coeff, remaining_digits):
    first_digit = decimal2snafu[coeff]
    lower = first_digit + "=" * remaining_digits
    upper = first_digit + "2" * remaining_digits

    return snafu_to_decimal(lower) <= number <= snafu_to_decimal(upper)


def decimal_to_snafu(number):
    ix = math.ceil(math.log(number, 5))
    remainder = number
    five_places = {jx: 0 for jx in range(ix)}

    while ix > 0:
        for coeff in [1, 2, -2, -1]:
            if in_snafu_range(remainder, coeff, ix):
                five_places[ix] = coeff
                remainder -= coeff * 5**ix
                break

        ix -= 1

    five_places[0] = remainder

    lijst = [v for (k, v) in sorted(five_places.items())]
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

    print("snafus      ", snafus)
    as_decimals = [snafu_to_decimal(s) for s in snafus]
    print("as decimals ", as_decimals)
    snafus_again = [decimal_to_snafu(d) for d in as_decimals]
    print("snafus again", snafus_again, snafus == snafus_again)

    total_decimal = sum(as_decimals)
    print("total decimal", total_decimal)
    part1 = decimal_to_snafu(total_decimal)

    print("part1:", part1)
    print("part2:", "start the blender")
    breakpoint()


day24(examples("25"))
day24(inputs("25"))
