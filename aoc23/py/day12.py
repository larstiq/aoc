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


@functools.cache
def multin(num, prefix):
    # Passing in num as a combination of '?' and '#', what could it be?
    # Maxmimum the number could be length
    options = []
    nuu = Counter(num)
    for ix in range(2**sum(c not in '01' for c in num)):
        # We need exactly two bits set, can skip the rest of the number.
        # Should this just be combinations of powers of 2?
        # Could pick all combinations of size k amon what?

        possible_replacement = bin(ix + 2**40)[-nuu['?']:]

        #if Counter(possible_replacement)['1'] != missing:
        #   continue

        ugh = num
        it = iter(possible_replacement)
        while "?" in ugh:
            ugh = ugh.replace("?", next(it), 1)

        #print(ugh)
        subcounts = [sum(1 for _ in group) for label, group in itertools.groupby(ugh) if label == '1']
        
        if subcounts == []:
            continue

        if subcounts == list(prefix[:len(subcounts)]):
            # Perhaps instead of passing multiple copies we can just counts?
            options.append(subcounts)
        else:
            print("Not", subcounts, "for", prefix, num)
    
    #breakpoint()
    return options


def score(springs):
    return [sum(1 for _ in group) for label, group in itertools.groupby(springs) if label == '1']

def admit(springs, prefix, left):
    subcounts = score(springs)
    # 1.1.1? is ok to have [1, 1, 1] <= [1, 1, 3]
    #if subcounts == [1, 1, 1]:
        #    breakpoint()

    # If we can't fill the missing it won't work

    missing_ones = sum(prefix) - Counter(springs)['1'] - Counter(left)['1']
    places_for_ones = Counter(left)['?']

    # In a contiguous ?1 block we can definitely not fit more than the amount of ?
    # as ones.  But if the len of the block is longer than prefix[0] we also need to spend some ? on separating 0.
    #
    #
    # So threshold is in fact  

# 101 1,1,3
#
#
    

    # sum(counts) - sum(1s_so_far) = to_place <= len(? left)
    if missing_ones > places_for_ones:
        return 0
    
    subprefix = prefix[:len(subcounts)]

    # On an exact match we can collapse all states into a count if we know the next character is not a ?
    if subcounts == subprefix:
        return 2
    elif subcounts[:-1] == subprefix[:-1] and subcounts[-1] < subprefix[-1]:
        return 1
    else:
        return 0


def prefix_admissable(prefix, full, sofar):
    subfull = tuple(full[:len(prefix)])

    # If the prefix has length N then there are N - 1 seperators
    #if sum(prefix) + len(prefix) - 1 > sofar:
    #    return 0

    if prefix[-1] > subfull[-1]:
        return 0
    elif prefix[:-1] == subfull[:-1]:
        return 1
    else:
        return 0


def progress(springs, counts):

    states = Counter()
    states[((), "0")] = 1

    aanelkaar = "0".join(springs)

    print(aanelkaar, counts)
    # TODO: instead of string concat this could be bitfields of some kind
    # Need to take care with encoding it as an integer because trailing zeros matter
    # Could store with an extra 1 or if we know the index exactly then it does not matter at all
#

    wehave = Counter(aanelkaar)
    total_unknown = wehave['?']
    to_fill = sum(counts) - wehave['1']
    left = aanelkaar

    for ix, char in enumerate(aanelkaar):
        print(ix, "/", len(aanelkaar), aanelkaar[:ix + 1])
        nextstates = Counter()
        #if states ==  {'00001', '10101', '00101'}:
        #    breakpoint()

        # States ending in zero can not increase their prefix anymore and we can simply count how many there are per prefix.
        # States ending in one  may branch and there is a difference between
        #
        # 1010
        # 1001 
        #
        # as the latter may develop into (1, 2) and the former may not
#
#  So our state space is (prefix, last char, count)  
#  This we can do with a counter on (prefix, last char)
#
#
#
        # ???0111  1, 1, 3
        # 0, 1     00: 1,  01: 1     (): 1,  (1,): 1
        # 00, 01, 10, 11   (), 0: 1,  
        # 000, 001, 010, 011, 100, 101, 110, 111

        for state, count in states.items():
            prefix, lastchar = state

            # (1, 1, 1) -> (1, 1, 2)

            if prefix == ():
                prefixplus = prefixand = (1,)
            else:
                prefixplus = prefix[:-1] + (prefix[-1] + 1,)
                prefixand = prefix + (1,)

            batch = Counter()

            match (lastchar, char):
                case "1", "1": # We extend a contiguous string of 1s with one more
                    if prefix_admissable(prefixplus, counts, ix + 1):
                        batch[(prefixplus, char)] += count
                case "0", "1": # Another contiguous batch starts
                    if prefix_admissable(prefixand, counts, ix + 1):
                        batch[(prefixand, char)] += count
                    
                case _, "0": # we continue, prefix remains admissable
                    batch[(prefix, "0")] += count
                case "1", "?": # We split
                    # Adding a terminating zero carries on the prefix
                    batch[(prefix, "0")] += count

                    # Adding a 1 either extends
                    batch[(prefixplus, "1")] += count
                case "0", "?": # We split
                    batch[(prefix, "0")] += count
                    # or lengthens
                    #breakpoint()
                    #if aanelkaar[:ix] == '?111????????':
                    #    breakpoint()
                    if prefix_admissable(prefixand, counts, ix + 1):
                        batch[(prefixand, "1")] += count

            nextstates += batch

        for pp in sorted(nextstates):
            print("    ", pp, nextstates[pp])
        #print("   ", sorted(states.items()), "->", sorted(nextstates.items()))
        states = nextstates

    print(states)
    #print(aanelkaar, counts)
    #breakpoint()

    return sum(count for ((prefix, lastchar), count) in states.items() if prefix == counts)


def day12(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    equal = 0
    unequal = 0
    solved = []
    unsolved = []
    parts = {}

    grandcounts = []
    replacings = []
    diffs = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            springs, counts = line.split()
            springs = "?".join(5 * [springs]).replace("#", "1")
            counts = ",".join(5 * [counts])
            counts = counts.split(",")
            kounts = tuple(map(int, counts))
            expanded = "0".join("1" * int(leng) for leng in counts) 

            tot = Counter(expanded)

            if "." in springs:
                knowns = [piece for piece in springs.split(".") if piece != '']
            else:
                knowns = [springs]

            grandcounts.append(progress(knowns, kounts))

    part1 = sum(grandcounts)
    print(grandcounts)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day12(examples("12"))
day12(inputs("12"))
