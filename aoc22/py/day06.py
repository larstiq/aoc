#!/usr/bin/env python

import collections
from itertools import islice

from utils import inputs, examples


# Copied from https://docs.python.org/3/library/itertools.html recipes
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def decode(line, size):
    for win in sliding_window(line, size):
        if len(set(win)) == size:
            return size + line.index("".join(win))



def day06(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:

        for line in puzzlein:
            print("part1", decode(line.strip(), 4))
            print("part2", decode(line.strip(), 14))

day06(inputs("06"))
day06(examples("06"))
