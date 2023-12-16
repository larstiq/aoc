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

    # What about a minimum? That depends on the placement no?

    # So now we're looking for decompositions 


def delve(remaining_springs, unmatched):
    # Assume that so far the prefix has matched.  Which pieces can further match the prefix?
    #breakpoint()

    if len(remaining_springs) == 0:
        return 0

    maybe_springs = remaining_springs[0]
    # Maybe springs is a combination of # and ?.  What numbers can this form?

    ways = []


    which_springs = Counter(maybe_springs) 
    undamaged_springs = which_springs["1"]
    firstk = unmatched[0]

    thresh = 0
    takek = 0
    for k in unmatched:
        if thresh > len(maybe_springs):
            break
        thresh += int(k)
        takek += 1

    # This might end up with too long a prefix,
    # say with "???" [1, 1, 3]

    # TODO: shortcut out of this in cases like
    # '111????? [1, 3, 1, 1], that is never going to work


    spring_prefix = 0
    for ix, char in enumerate(maybe_springs):
        if char != '1':
            spring_prefix = ix + 1
            if spring_prefix > unmatched[0]:
                return 0
            break

    pass_prefix = tuple(unmatched[:takek])
    assert sum(pass_prefix) >= len(maybe_springs)

    # When does this fail?
    # assert sum(pass_prefix[:-1]) < len(maybe_springs)
    #breakpoint()


    for prefix in multin(maybe_springs, pass_prefix):
        # If this can be a legit prefix, look at the other possible options
        if prefix == unmatched[:len(prefix)]:
            rest = remaining_springs[1:]
            if rest == []:
                continue

            # What should we peel off? Given a group of maybe damaged spring '#?#?' and a prefix [k1, k2, k3, ],
            # There can be at most len(maybe_springs) springs in there, so we at most consume from the prefix [k1, ..., kn]
            # so that sum (k1, ... kn-1) < len(maybe_springs) and sum(k1 ... kn) >= len(maybe_springs)  
            #
            # Likewise we'll consume at most a block such that sum(1 in maybe_springs) >= k1

            options = delve(remaining_springs[1:], unmatched[len(prefix):]))
            # TODO: we can't strip off the prefix', '???.111???' (1, 1, 3) would fail
            # if ??? is matched with (1,), it needs to be (1, 1) for the rest to make sense.
            ways.append(

    print("Delve ended for", remaining_springs, unmatched, ways)
    return sum(ways)





    print(line, options, len(options))
    grandcounts.append(len(options))

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
            kounts = list(map(int, counts))
            expanded = "0".join("1" * int(leng) for leng in counts) 

            tot = Counter(expanded)

            if "." in springs:
                knowns = [piece for piece in springs.split(".") if piece != '']
            else:
                knowns = springs

            grandcounts.append(delve(knowns, list(map(int, counts))))




    part1 = sum(grandcounts)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day12(examples("12"))
day12(inputs("12"))
