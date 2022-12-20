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
    touched: bool

def day20(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0
    data = np.loadtxt(filename, dtype=int)

    #data = [1, 3, 4, -5]
    print(data)



    positions = [Positioned(v, False) for v in data]


    #breakpoint()
    while True:

        for jx, pos in enumerate(positions):
            if pos.touched:
                continue
            break
        else:
            break

        assert positions[jx] == pos

        if "example" in str(filename):

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

        # For 4 we need len(data), why -1 in the other case? Is it on the negativity?


        removed = False

        if pos.value > 0:
            new_index = (jx + pos.value) % len(data)
        elif pos.value < 0:
            new_index = (jx + pos.value) % (len(data) - 1)
        elif pos.value == 0:
            pos.touched = True
            removed = True
            print("    Positioning", pos, "currently at", jx, "then", new_index)
            #print([pos.value for pos in positions])
            continue


        #  If we're moving the item to the left or right by less than len(data) we're not skippg over ourselves
        #
        #       0  1  2  3  4
        #  -5: [1, |, 2, 4, 5]  2 + -5
        #  -4: [1, 2, |, 4, 5]
        #  -3: [1, 2, 4, |, 5]
        #  -2: [|, 1, 2, 4, 5]
        #  -1: [1, |, 2, 4, 5]
        #   0: [1, 2, |, 4, 5]
        #   1: [1, 2, 4, |, 5]
        #  +2: [1, 2, 4, 5, |]
        #  +3: [1, |, 2, 4, 5]
        #  +4: [1, 2, |, 4, 5]
        #  +5: [1, 2, 4, |, 5]
        # 

        #
        # [1, 2, -3, 0, 3, 4, -2]
        #                  5      6 7 8 9
        #  6  7   8  9

        # TODO: would this be easier if we had space between the items? ix |-> 2*x

        # Careful, changes the positioning
        #print("    Positioning", pos, "currently at", jx, "then", new_index)

        if 0 < new_index < len(data) - 1:
            positions[new_index:new_index+1] = [
                positions[new_index],
                Positioned(pos.value,  True),
            ]
        elif new_index == 0:
            positions.append(Positioned(pos.value, True))
        else:
            breakpoint()
            assert new_index == len(data) - 1
            positions.append(Positioned(pos.value, True))

        if not removed:
            positions.remove(pos)

        
        #print([(pos.value, pos.touched) for pos in positions])
        #print([pos.value for pos in positions])


    (zix, zero_pos), = [(ix, p) for (ix, p) in enumerate(positions) if p.value == 0]

    breakpoint()
    print([positions[ix % len(data)].value for ix in (zix + 1000, zix + 2000, zix + 3000)])

    enc = sum(positions[ix % len(data)].value for ix in (zix + 1000, zix + 2000, zix + 3000))

    print("part1:", enc)
    print("part2:", part2)
    #:w breakpoint()


day20(examples("20"))
day20(inputs("20"))
