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


# This should also be doable with plain math
@functools.cache
def options_questions(damage_length):
    # Given `damage_length` damaged spring records how many strings of # and . can we fit?
    #
    # The Bell numbers count the number of set partitions, but we only allow contiguous groupings.
    #
    # But using the stars and bars argument we can divide N damaged records into k groups by placing
    # the k bars in the N-1 gaps between stars. Since # and . alternate and
    # there is at least one star between bars this gives e.g.
    #
    #
    # ? ? ? | ? | ? ? | ? ? ?     N=9, k=3 either ###.##... or ...#..###.  Theare are (8 choose 3) total groupings into four groups.
    #
    # T

    #
    # The first spring could be . or 
    #
    # Returns a dictionary with {(n1, n2, ...nm), head, tail: count} that says there
    # are `count` instances of contiguous (n1, n2, ..., nm) that start with
    # `head` and end with `tail`.
    result = Counter()

    if damage_length == 2:
        result[(), '.', '.''] = 1
        result[(1,), '#'] = 1
        return result

    for (prefix, head, tail), count in damage_length(damage_length - 1):
        # Branch starting with '.' carries on the prefix
        result[(prefix, '.')] += count
        match head, tail:
            case '#':
                if prefix == ():
                    extended = (1,)
                else:
                    extended = (prefix[0] + 1,) + prefix[1:]
                # Ours is #
                result[(extended, '#')] += count
                # or .
            case '.':
                concatted = prefix + (1,)
                result[(concatted, '#')] += count
    return result
    

def concat(prefix: tuple[int, ...], suffix: tuple[int, ...]):
    return prefix + suffix
    

# We need to extend both left and right
def extend(prefix: tuple[int, ...], suffix: tuple[int, ...]):
    return prefix[:-1] + (prefix[-1] + suffix[0],) + suffix[1:]


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
            suffix = (len(group),)

            batch = Counter()
            match (lastchar, char):
                case "#", "#": # We extend a contiguous string of #s
                    batch[extend(prefix, suffix), char)] += count
                case ".", "#": # Another contiguous string starts
                    batch[(concat(prefix, suffix)), char)] += count
                case _, ".": # we continue, prefix remains admissable
                    batch[(prefix, ".")] += count
                case _, "?": # Damaged records split in two branches
                    # The branch adding a terminating . carries on the prefix
                    batch[(prefix, ".")] += count

                    # For a block of damaged records iterate over the possible
                    # damage suffixes
                    for (duffix,  duffix_start), duffix_count in options_questions(len(group)):
                        # The branch adding a # either
                        match lastchar, duffix_start:
                            case '#', '.':
                                # Concat
                                batch[concat(prefix, duffix), 
                            case '#', '#':
                                pass
                            case '.', '.':
                                pass
                            case '.', '#':

                            case '#':
                                # extends a contiguous string of #
                                batch[extend(prefixplus, "#")] += count
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
