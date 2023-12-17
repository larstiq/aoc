#!/usr/bin/env python

from collections import Counter
from itertools import groupby
from time import time

from utils import examples, inputs



def prefix_admissable(prefix, full):
    subfull = tuple(full[:len(prefix)])

    if prefix[-1] > subfull[-1]:
        return 0
    elif prefix[:-1] == subfull[:-1]:
        return 1
    else:
        return 0


def error_correct(springs, counts):
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

    # TODO: split on blocks of contiguous characters:
    #  .....  keeps the state the same
    #  #####  maps prefix (..., N)  to (..., N + count of 3)
    #  ?????  use integer partitions with stars and bars to give the counts of
    #         (n, k) tuples that arise to permissible prefixes
    for (char, group) in groupby(springs):
        nextstates = Counter()

        for state, count in states.items():
            prefix, lastchar = state
            if prefix == ():
                prefixplus = prefixand = (len(group),)
            else:
                prefixplus = prefix[:-1] + (prefix[-1] + len(group),)
                prefixand = prefix + (len(group),)

            batch = Counter()
            match (lastchar, char):
                case "#", "#": # We extend a contiguous string of #s
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
        index += 1

    return sum(count for ((prefix, lastchar), count) in states.items() if prefix == counts)


def day12(filename):
    print()
    print(filename)
    start = time()

    part1 = 0
    part2 = 0

    grandcounts = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            springs, counts = line.split()
            counts = tuple(map(int, counts.split(",")))

            part1 += error_correct(springs, counts)
            part2 += error_correct("?".join(5 * [springs]), counts * 5)

    print("time:", time() - start)
    print("part1:", part1)
    print("part2:", part2)

    if str(filename).endswith("inputs/12"):
        assert part1 == 7939
        assert part2 == 850504257483930


day12(examples("12"))
day12(inputs("12"))
