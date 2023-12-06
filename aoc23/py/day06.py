#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx


def day06(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    times = []
    distances = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            left, right = line.split(":")
            if left == "Time":
                times.extend(map(int, right.split()))
            if left == "Distance":
                distances.extend(map(int, right.split()))


    times = [56717999]
    distances = [334113513502430]
    wins = []
    for ix, time in enumerate(times):
        # Charge all the time won't move
        local_wins = 0
        for y in range(time):
            if (time - y) * y > distances[ix]:
                local_wins += 1

        #sum(1 to N, (N - x)*x) = sum(1 to N) x*N - x*2 = N * sum (1 to N) x - sum(1 to N) x*2

        wins.append(local_wins)

    part1 = wins
    print(times, distances)
    print("part1:", part1)
    print("part2:", part2)


day06(examples("06"))
day06(inputs("06"))
