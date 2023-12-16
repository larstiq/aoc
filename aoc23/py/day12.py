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

    # sum(counts) - sum(1s_so_far) = to_place <= len(? left)
    if missing_ones > places_for_ones:
        return 0
    
    subprefix = prefix[:len(subcounts)]
    if subcounts == subprefix:
        return 1
    elif subcounts[:-1] == subprefix[:-1] and subcounts[-1] < subprefix[-1]:
        return 1
    else:
        return 0

def progress(springs, counts):

    states = {""}

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
        print(springs, ix, len(aanelkaar))
        nextstates = set()
        #if states ==  {'00001', '10101', '00101'}:
        #    breakpoint()
        for state in states:
            batch = set()
            if char == "1": 
                batch.add(state + "1")
            elif char == "0":
                batch.add(state + "0")
            elif char == "?":
                total_unknown -= 1
                batch.add(state + "1")
                batch.add(state + "0")

            nextstates |= {st for st in batch if admit(st, counts, left)}

        left = left[1:]
        #print(ix, char, states, "->", [(score(n), n) for n in nextstates])
        #breakpoint()
        states = nextstates

    trim_states = {n for n in nextstates if score(n) == counts}
    print(springs, len(nextstates), len(trim_states))
    #print(aanelkaar, counts)
    #breakpoint()
    return len(trim_states)


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
                knowns = [springs]

            grandcounts.append(progress(knowns, kounts))

    part1 = sum(grandcounts)
    print(grandcounts)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day12(examples("12"))
day12(inputs("12"))
