#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx

import itertools

def day07(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    mapping = dict(zip(reversed("AKQJT98765432"), itertools.count()))
    back = {v: k for (k, v) in mapping.items()}
    hands = {}
    with open(filename) as puzzlein:
        for line in puzzlein:
            hand, bid = line.strip().split()
            hand = tuple([mapping[c] for c in hand])
            hands[hand] = int(bid)


    def rank(left, right):
        l = Counter(left)
        r = Counter(right)
        if l < r:
            return -1
        elif l > r:
            return 1
        else:
            return -1 * (mapping[left[0]] > mapping[right[0]])


    def key(c):
        twee = list(reversed(sorted(Counter(c).values())))[:2]
        if len(twee) < 2:
            twee.append(0)
        twee.append(c)
        return twee

    import functools
    sorte = list(hands.keys())
    sorte.sort(key=key)
    print(sorte)
    #:w
    # sorte.sort(key=functools.cmp_to_key(rank))

    backed = ["".join(back[c] for c in h) for h in sorte]
    print(backed)

    winnings = [(ix + 1)*hands[hand] for ix, hand in enumerate(sorte)]
    
    part1 = sum(winnings)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day07(examples("07"))
day07(inputs("07"))
