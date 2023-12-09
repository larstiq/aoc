#!/usr/bin/env python

from utils import examples, inputs

import numpy as np


def day09(filename):
    print()
    print(filename)

    histories = np.loadtxt(filename, dtype=int)

    def delve(history):
        next_level = np.diff(history)
        deeper = delve(next_level) if next_level.any() else 0
        return history[-1] + deeper

    part1 = sum(delve(line) for line in histories)
    part2 = sum(delve(line[::-1]) for line in histories)

    print("part1:", part1)
    print("part2:", part2)


day09(examples("09"))
day09(inputs("09"))
