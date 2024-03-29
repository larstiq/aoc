#!/usr/bin/env python

from collections import Counter
from utils import examples, inputs, display_dfield

from heapq import heappush, heappop

from time import time


def day17(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(list(map(int, line.strip())))

    stop = len(data) - 1, len(data[0]) - 1
    UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

    TURNS = {
        UP: [LEFT, RIGHT],
        DOWN: [RIGHT, LEFT],
        LEFT: [UP, DOWN],
        RIGHT: [
            DOWN,
            UP,
        ],
    }

    def drive_crucible(moverange):
        start = time()
        states = Counter()
        states[0, 0, DOWN] = 0
        states[0, 0, RIGHT] = 0

        heads = [(loss,) + state for (state, loss) in states.items()]
        while len(heads) > 0:
            state = heappop(heads)
            state_loss, px, py, direction = state
            dx, dy = direction
            additional_loss = 0

            if (px, py) == stop:
                break

            # Avoid tracking amount of steps by adding all possible reached squares
            # after we turn.
            #
            # Ultracrucible can take at most 10 steps
            for step in range(1, moverange.stop):
                x, y = px + step * dx, py + step * dy

                # Since we're casting into the same direction, if we're out of
                # bends after step N we'll be more out of bounds at step N+1,
                # terminate the entire ray early.
                if not (0 <= x <= stop[1] and 0 <= y <= stop[0]):
                    break

                additional_loss += data[y][x]
                loss = state_loss + additional_loss

                # Ultracrucible can not turn before step 4, but accumulated losses
                # should be tracked
                if step < moverange.start:
                    continue

                for turn in TURNS[direction]:
                    if (x, y, turn) in states and states[x, y, turn] <= loss:
                        continue

                    heappush(heads, (loss, x, y, turn))
                    states[x, y, turn] = loss

        print("time:", time() - start)
        return state_loss


    part1 = drive_crucible(range(1, 4))
    part2 = drive_crucible(range(4, 11))

    print("part1:", part1)
    print("part2:", part2)


day17(examples("17-2"))
day17(examples("17"))
day17(inputs("17"))
