#!/usr/bin/env python

from utils import inputs, examples

import pandas as pd
import collections


def day09(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    instructions = []
    with open(filename) as puzzlein:
        # TODO shaping
        for line in puzzlein:
            direction, step = line.strip().split()
            step = int(step)
            instructions.append((direction, step))

    head, tail = (0, 0), (0, 0)

    seen_tails = set([tail])
    visits = pd.DataFrame(data=[['.'] * 1200 for i in range(1200)], index=range(-600, 600), columns=range(-600, 600))
    visits.loc[0][0] = 's'
    print(visits)
    #breakpoint()
    for instr in instructions:
        direction, step = instr
        print(instr)
        for s in range(step):
            if direction == "R":
                head = head[0], head[1] + 1
            if direction == "U":
                head = head[0] - 1, head[1]
            if direction == "L":
                head = head[0], head[1] - 1
            if direction == "D":
                head = head[0] + 1, head[1]

            visits.loc[head[0]][head[1]] = 'H'
            #print(visits)
            #breakpoint()
            body = head[0] - tail[0], head[1] - tail[1]
            print("body", body)
            if sorted(map(abs, body)) in [[0, 0], [0, 1], [1, 1]]:
                # Touching, nevermind
                print("touching", head, tail)
                continue

            print("body after touching", body)

            if body in [(0, 2)]:
                tail = tail[0], tail[1] + 1
            elif body in [(0, -2)]:
                tail = tail[0], tail[1] - 1
            elif body in [(2, 0)]:
                tail = tail[0] + 1, tail[1]
            elif body in [(-2, 0)]:
                tail = tail[0] - 1, tail[1]
            else:
                # Diagonal step
                # math.copysign?
                diff = [None, None]
                if body[0] > 0:
                    diff[0] = 1
                else:
                    diff[0] = -1
                if body[1] > 0:
                    diff[1] = 1
                else:
                    diff[1] = -1
                print("diagonal case", head, tail, body, diff)
                tail = tail[0] + diff[0], tail[1] + diff[1]

            seen_tails.add(tail)
            visits.loc[tail[0]][tail[1]] = 'T'

    part1 = len(seen_tails)

    if True:
        max_row = max(t[0] for t in seen_tails)
        min_row = min(t[0] for t in seen_tails)
        max_col= max(t[1] for t in seen_tails)
        min_col = min(t[1] for t in seen_tails)

        #data = pd.DataFrame(
        #    index=range(min_col, max_col + 1),
        #    data=[['.' for x in range(min_row, max_row + 1) ]
        #                          for y in range(min_col, max_col + 1)])
        data = pd.DataFrame(data=[["."] * visits.shape[0]] * visits.shape[1], index=visits.index, columns=visits.columns)

        for t in seen_tails:
                data.loc[t[0]][t[1]] = '#'

    print(visits)
    print(data)
    print("part1:", part1)
    print("part2:", part2)


day09(inputs("09"))
#day09(examples("09"))
