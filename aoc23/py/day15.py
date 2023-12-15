#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math
import functools


def HASH(s):
    current = 0
    for char in s:
        current += ord(char)
        current *= 17
        current %= 256
    return current
   # return functools.reduce(lambda x, y: (x + ord(y) * 17) % 256, list(s), 0)

def day15(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    commands = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            commands.extend(line.strip().split(","))
            data.append(list(line.strip()))


    df = pd.DataFrame(data)


    hashes = []
    for part in commands:
        hashes.append(HASH(part))

    part1 = sum(hashes)
    print("part1:", part1)
    print("part2:", part2)


day15(examples("15"))
day15(inputs("15"))
