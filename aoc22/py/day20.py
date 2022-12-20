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

            if False and "example" in str(filename):
                if pos.value == 3:
                    assert [1, 2, 3, -2, -3, 0, 4] == [pos.value for pos in positions]
                    print("Good up to 3")

                if pos.value == -2:
                    assert [1, 2, -2, -3, 0, 3, 4] == [pos.value for pos in positions]
                    breakpoint()
                    print("Good up to -2")

                if pos.value == 0:
                    assert [1, 2, -3, 0, 3, 4, -2] == [pos.value for pos in positions]
                    print("Good up to 0")

                if pos.value == 4:
                    breakpoint()


            if pos.value == 0:
                positions.append(pos)
            else:
                new_index = pos.value % (N - 1)
                positions.insert(new_index, pos)

            largest_mixed += 1
            touched.add(pos.orig)
            #print(largest_mixed)

        print(times, [pos.value for pos in positions])

    (zix, zero_pos), = [(ix, p) for (ix, p) in enumerate(positions) if p.value == 0]

    breakpoint()
    print([positions[ix % len(data)].value for ix in (zix + 1000, zix + 2000, zix + 3000)])

    enc = sum(positions[ix % len(data)].value for ix in (zix + 1000, zix + 2000, zix + 3000))

    print("part1:", enc)
    print("part2:", part2)
    #:w breakpoint()


day20(examples("20"))
day20(inputs("20"))
