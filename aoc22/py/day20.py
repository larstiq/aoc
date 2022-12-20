#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict, deque
import time

import numpy as np
import re

from dataclasses import dataclass


@dataclass
class Positioned:
    value: int
    orig: int

def day20(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0
    data = list(811589153 * np.loadtxt(filename, dtype=int))

    print(data)

    positions = deque([Positioned(v, ix) for ix, v in enumerate(data)])

    N = len(positions)
    for times in range(10):
        touched = set()
        largest_mixed = -1
        while len(touched) < N:
            tip = positions.popleft()
            pos = tip
            if tip.orig != largest_mixed + 1:
                positions.append(tip)
                continue

            if pos.value == 0:
                positions.append(pos)
            else:
                new_index = pos.value % (N - 1)
                positions.insert(new_index, pos)

            largest_mixed += 1
            touched.add(pos.orig)

        print(times, [pos.value for pos in positions])

    (zix, zero_pos), = [(ix, p) for (ix, p) in enumerate(positions) if p.value == 0]

    breakpoint()
    print([positions[ix % len(data)].value for ix in (zix + 1000, zix + 2000, zix + 3000)])

    enc = sum(positions[ix % len(data)].value for ix in (zix + 1000, zix + 2000, zix + 3000))

    print("part1:", enc)
    print("part2:", part2)


day20(examples("20"))
day20(inputs("20"))
