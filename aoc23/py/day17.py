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
    # More than needed but they will be pruned, so just eliminate
    # a chance of me getting the naming wrong
    states[start, DOWN] = 0
    states[start, RIGHT] =  0
    states[start, UP] = 0
    states[start, LEFT] =  0
    heads = { h for h in states }
    path = pd.DataFrame(data=np.nan, index=df.index, columns=df.columns, dtype=object)

    TURNS = {
            UP: [LEFT, RIGHT],
            DOWN: [RIGHT, LEFT],
            LEFT: [UP, DOWN],
            RIGHT: [DOWN, UP,]
            }
    DEBUG = False
    while len(heads) > 0:
        prevstates = states.copy()
        prevheads = heads.copy()
        #print("Heads:", heads)

        touched = set()
        for state in heads:
            # We can take at most 3 steps, let's add them all so we don't need
            # to think in the next step but just take the turns
            
            state_loss = states[state]
            pos, direction = state

            additional_loss = 0
            for ix in range(1, 4):
                npos = pos[0] + ix*direction[0], pos[1] + ix*direction[1]
                if npos[0] not in df.index or npos[1] not in df.columns:
                    continue

                additional_loss += df[npos[1]][npos[0]]
                loss = state_loss + additional_loss

                for turn in TURNS[direction]:
                    if (npos, turn) in states and states[npos, turn] < loss:
                        continue

                    touched.add((npos, turn))
                    states[npos, turn] = loss

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

        heads = { h for h in touched if states[h] <= prevstates[h]}
        heads = touched
        if DEBUG:
            display_dfield(path)
            endstates = {state for state in states if state[0] == stop }
            if len(endstates) > 0:
                print(min(states[s] for s in endstates)) 

            prevlosses = pd.DataFrame(data=np.nan, index=df.index, columns=df.columns)

            for state in prevstates:
                there = prevlosses[state[0][1]][state[0][0]] 
                prevlosses[state[0][1]][state[0][0]] = np.nanmin([there, prevstates[state]])

            curlosses = pd.DataFrame(data=np.nan, index=df.index, columns=df.columns)
            for state in states:
                there = curlosses[state[0][1]][state[0][0]]
                curlosses[state[0][1]][state[0][0]] = np.nanmin([there, states[state]])

        if heads.issubset(prevheads):
            break

        print(len(heads))

    endstates = {state for state in states if state[0] == stop }
    part1 = min(states[s] for s in endstates)

    print("Too high?", part1 >= 860)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day17(examples("17"))
day17(inputs("17"))
