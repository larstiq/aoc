#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs, display_dfield

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math


def day17(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(list(map(int, line.strip())))

    df = pd.DataFrame(data)
    start = (0, 0)
    stop = df.shape[0] - 1, df.shape[1] - 1

    UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
    states = Counter()
    states[start, DOWN, 0] = 0
    states[start, RIGHT, 0] =  0
    heads = { h for h in states }
    path = pd.DataFrame(data=np.nan, index=df.index, columns=df.columns, dtype=object)

    TURNS = {
            UP: [LEFT, RIGHT],
            DOWN: [LEFT, RIGHT],
            LEFT: [UP, DOWN],
            RIGHT: [UP, DOWN,]
            }
    DEBUG = False
    while len(heads) > 0:
        prevstates = states.copy()
        #print("Heads:", heads)

        touched = set()
        for state in heads:
            # We can take at most 3 steps, let's add them all so we don't need
            # to think in the next step but just take the turns
            
            state_loss = states[state]
            pos, direction, steps = state

            additional_loss = 0
            for ix in range(1, 4):
                npos = pos[0] + ix*direction[0], pos[1] + ix*direction[1]
                if npos[0] not in df.index or npos[1] not in df.columns:
                    continue

                additional_loss += df[npos[1]][npos[0]]
                loss = state_loss + additional_loss

                for turn in TURNS[direction]:
                    if (npos, turn, ix) in states and states[npos, turn, ix] < loss:
                        continue

                    touched.add((npos, turn, ix))
                    states[npos, turn, ix] = loss

                    if DEBUG:
                        if direction == RIGHT:
                            angle = '>'
                        elif direction == UP:
                            angle = '^'
                        elif direction == LEFT:
                            angle = '<'
                        elif direction == DOWN:
                            angle = 'v'

                        path[npos[1]][npos[0]] = angle

        #display_dfield(path)
        heads = { h for h in touched if states[h] >= prevstates[h]}
        print(len(heads))

    endstates = {state for state in states if state[0] == stop }
    part1 = min(states[s] for s in endstates)

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day17(examples("17"))
day17(inputs("17"))
