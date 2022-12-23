#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict, deque
import time

import numpy as np
import re

import networkx as nx
import sympy

from dataclasses import dataclass


def day23(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    with open(filename) as puzzlein:
        for line in puzzlein:

    print("part1:", part1)
    print("part2:", part2)


day23(examples("23"))
day23(inputs("23"))
