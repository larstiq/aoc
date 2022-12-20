#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict
import time

import numpy as np
import re

from dataclasses import dataclass


@dataclass
class Positioned:
    value: int
    orig_pos: int
    touched: bool

def day20(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0
    data = np.loadtxt(filename, dtype=int)

    print(data)



    positions = [Positioned(v, ix, False) for ix, v in enumerate(data)]


    #breakpoint()
    while True:

        for jx, pos in enumerate(positions):
            if pos.touched:
                continue
            break
        else:
            break

        assert positions[jx] == pos

        if pos.value == 3:
            assert [1, 2, 3, -2, -3, 0, 4] == [pos.value for pos in positions]
            print("Good up to 3")

        if pos.value == -2:
            assert [1, 2, -2, -3, 0, 3, 4] == [pos.value for pos in positions]
            print("Good up to -2")


        if pos.value == 0:
            pos.touched = True
            continue

        new_index = (jx + pos.value) % len(data)

        # Careful, changes the positioning
        print("    Positioning", pos, "currently at", jx)
        removed = False

        if abs(pos.value) > len(data):
            breakpoint()
            positions.remove(pos)

        if 0 < new_index < len(data) - 1:
            if pos.value > 0:
                positions[new_index:new_index+1] = [
                    positions[new_index],
                    Positioned(pos.value, pos.orig_pos, True),
                ]
            else:
                positions[new_index:new_index+1] = [
                    Positioned(pos.value, pos.orig_pos, True),
                    positions[new_index],
                ]
        else:
            if new_index == 0:
                positions.append(Positioned(pos.value, pos.orig_pos, True))
                positions.remove(pos)
                continue
            elif new_index == len(data) - 1:
                positions = [Positioned(pos.value, pos.orig_pos, True)] + positions
                positions.remove(pos)
                continue

            breakpoint()
            if pos.value > 0:
                positions[new_index:new_index+1] = [
                    positions[new_index],
                    Positioned(pos.value, pos.orig_pos, True),
                ]
            else:
                positions[new_index:new_index+1] = [
                    Positioned(pos.value, pos.orig_pos, True),
                    positions[new_index],
                ]


        if not removed:
            positions.remove(pos)

        
        #print([(pos.value, pos.touched) for pos in positions])
        print([pos.value for pos in positions])


    (zix, zero_pos), = [(ix, p) for (ix, p) in enumerate(positions) if p.value == 0]

    breakpoint()
    enc = sum(positions[ix % len(data)].value for ix in (zix + 1000, zix + 2000, zix + 3000))

    print("part1:", enc)
    print("part2:", part2)
    #:w breakpoint()


day20(examples("20"))
#day20(inputs("20"))
