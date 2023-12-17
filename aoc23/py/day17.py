#!/usr/bin/env python

from collections import Counter
from utils import examples, inputs, display_dfield

import pandas as pd

from heapq import heappush, heappop

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

    stringdf = pd.DataFrame([map(str, row) for row in data])
    start = (0, 0)
    stop = df.shape[0] - 1, df.shape[1] - 1

    UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
    states = Counter()
    states[start, DOWN] = 0
    states[start, RIGHT] = 0

    heads = [(loss, state[0], state[1]) for (state, loss) in states.items()]

    TURNS = {
            UP: [LEFT, RIGHT],
            DOWN: [RIGHT, LEFT],
            LEFT: [UP, DOWN],
            RIGHT: [DOWN, UP,]
            }
    DEBUG = False

    while len(heads) > 0:
        # Avoid tracking amount of steps by adding all possible reached squares
        # after we turn
        
        state = heappop(heads)
        state_loss, pos, direction = state
        additional_loss = 0

        # Ultracrucible
        for ix in range(1, 11):
            npos = pos[0] + ix*direction[0], pos[1] + ix*direction[1]

            # Since we're casting into the same direction, if we're out of
            # bends after step N we'll be more out of bounds at step N+1,
            # terminate the entire ray early.
            if npos[0] not in df.index or npos[1] not in df.columns:
                break

            additional_loss += df[npos[1]][npos[0]]
            loss = state_loss + additional_loss

            # Ultracrucible can not turn before step 4, but accumulated losses
            # should be tracked
            if ix < 4:
                continue

            for turn in TURNS[direction]:
                if (npos, turn) in states and states[npos, turn] <= loss:
                    continue

                heappush(heads, (loss, npos, turn))
                states[npos, turn] = loss

    endstates = {state for state in states if state[0] == stop }
    part1 = min(states[s] for s in endstates)

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day17(examples("17-2"))
day17(examples("17"))
day17(inputs("17"))
