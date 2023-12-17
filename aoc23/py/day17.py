#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

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

    UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
    states = Counter()
    states[start, DOWN, 0] = 0
    states[start, RIGHT, 0] =  0
    heads = { h for h in states }

    minloss = None
    while len(heads) > 0:
        prevstates = states.copy()
        print("Heads:", heads)
        for state in heads:
            # We can take at most 3 steps, let's add them all so we don't need
            # to think in the next step but just take the turns
            batch = Counter()
            
            state_loss = states[state]
            pos, direction, steps = state

            loss = 0
            for ix in range(4):
                npos = pos[0] + ix*direction[0], pos[1] + ix*direction[1]
                if npos[0] not in df.index or npos[1] not in df.columns:
                    continue

                if ix != 0:
                    loss += df[npos[1]][npos[0]]
                    print(npos, loss)
                elif steps == 0:
                    continue
                if direction == UP:
                    batch[npos, LEFT, ix] = state_loss + loss
                    batch[npos, RIGHT, ix] = state_loss + loss
                elif direction == DOWN:
                    batch[npos, LEFT, ix] = state_loss + loss
                    batch[npos, RIGHT, ix] = state_loss + loss
                elif direction == LEFT:
                    batch[npos, UP, ix] = state_loss + loss
                    batch[npos, DOWN, ix] = state_loss + loss
                elif direction == RIGHT:
                    batch[npos, UP, ix] = state_loss + loss
                    batch[npos, DOWN, ix] = state_loss + loss

            for ding in batch:
                print("   ", ding, batch[ding])
            for (nnpos, dire, steps), nloss in batch.items():
                if (nnpos, dire, steps) in states:
                    states[nnpos, dire, steps] = min(states[nnpos, dire, steps], nloss)
                else:
                    states[nnpos, dire, steps] = nloss

        heads = { h for h in states if states[h] > prevstates[h] }

    endstates = {(poss, dird, steps) for  (poss, dird, steps) in states if poss == (df.shape[0] - 1, df.shape[1] - 1) }
    part1 = min(states[s] for s in endstates)

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day17(examples("17"))
day17(inputs("17"))
