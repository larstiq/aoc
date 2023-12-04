#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx


def day04(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    cards = {}
    with open(filename) as puzzlein:
        for line in puzzlein:
            left, right = line.strip().split(":")
            cid = int(left.split()[1])

            left, right = right.split("|")
            win = { int(x) for x in left.split() }
            have = { int(x) for x in right.split() }
            cards[cid] = (win, have)


    points = []
    for (win, have) in cards.values():
        inter = len(win.intersection(have))
        if inter > 0:
            points.append(2**(inter - 1))

    part1 = sum(points)

    print("part1:", part1)
    print("part2:", part2)


day04(examples("04"))
day04(inputs("04"))
