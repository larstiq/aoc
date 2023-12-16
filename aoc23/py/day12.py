#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math
import re
import exrex
import functools


def prefix_admissable(prefix, full):
    subfull = tuple(full[:len(prefix)])

    if prefix[-1] > subfull[-1]:
        return 0
    elif prefix[:-1] == subfull[:-1]:
        return 1
    else:
        return 0


def progress(springs, counts):
    # We can collapse strings of ... to . as they won't contribute
    # to contiguous ones
    reduced = ".".join(s for s in springs.split(".") if s != '')

    # States ending in . can not increase their prefix anymore and we can simply count how many there are per prefix.
    # States ending in #  may branch and there is a difference between
    #
    #   #.#.
    #   #..# 
    #
    # as the latter may develop into (1, 2) and the former may not
    # So our state space is (prefix, last char, count)  
    states = Counter()
    states[((), ".")] = 1

    for ix, char in enumerate(reduced):
        nextstates = Counter()

        for state, count in states.items():
            prefix, lastchar = state
            if prefix == ():
                prefixplus = prefixand = (1,)
            else:
                prefixplus = prefix[:-1] + (prefix[-1] + 1,)
                prefixand = prefix + (1,)

            batch = Counter()
            match (lastchar, char):
                case "#", "#": # We extend a contiguous string of #s with one more
                    batch[(prefixplus, char)] += count
                case ".", "#": # Another contiguous string starts
                    batch[(prefixand, char)] += count
                case _, ".": # we continue, prefix remains admissable
                    batch[(prefix, ".")] += count
                case _, "?": # Damaged records split in two branches
                    # The branch adding a terminating . carries on the prefix
                    batch[(prefix, ".")] += count

                    # The branch adding a # either
                    match lastchar:
                        case '#':
                            # extends a contiguous string of #
                            batch[(prefixplus, "#")] += count
                        case '.':
                            # or starts another
                            batch[(prefixand, "#")] += count

            # Prune illegal states.
            for (nextprefix, lc), ncount in batch.items():
                if nextprefix == () or prefix_admissable(nextprefix, counts):
                    nextstates[(nextprefix, lc)] += ncount

        states = nextstates

    return sum(count for ((prefix, lastchar), count) in states.items() if prefix == counts)


def day12(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    grandcounts = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            springs, counts = line.split()
            counts = tuple(map(int, counts.split(",")))

            part1 += progress(springs, counts)
            part2 += progress("?".join(5 * [springs]), counts * 5)
            #print(line, progress("?".join(5 * [springs]), counts * 5))

    print("part1:", part1)
    print("part2:", part2)


day12(examples("12"))
day12(inputs("12"))
