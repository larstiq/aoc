#!/usr/bin/env python

from utils import inputs, examples

import pandas as pd
import collections
import itertools


def day10(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0


    instructions = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            if line == "noop":
                instructions.append((1, "noop"))
            else:
                left, right = line.split()
                instructions.append((2, left, int(right)))

    instructions.reverse()


    registers = {"X": 1}

    last_instr = 0
    signal_strengths = []
    for cycle in itertools.count(start=1):
        # TODO: do we need to begin and end execution?
        #print(instructions)
        #print(cycle, last_instr, len(instructions), instructions[-1])

        #if 218 <= cycle <= 220:
            #    breakpoint()
        if cycle % 20 == 0:
            signal_strengths.append((cycle, registers["X"]))

        if cycle == last_instr + instructions[-1][0]:
            instr = instructions.pop()
            last_instr = cycle
            if instr[1] == "noop":
                pass
            if instr[1] == "addx":
                registers["X"] += instr[2]

                #else:
                #    if cycle > 50:
                #        breakpoint()

        # Where is the sprite
        X = registers["X"]
        if cycle % 40 in (X - 1, X, X + 1):
            print("#", end='')
        else:
            print(".", end='')
        if cycle % 40 == 0:
            print()



        if len(instructions) == 0:
            break
        

    print(signal_strengths)
    print("part1:", sum(cycle * X for (cycle, X) in signal_strengths if cycle in (20, 60, 100, 140, 180, 220)))
    print("part2:", part2)


day10(inputs("10"))
day10(examples("10"))
