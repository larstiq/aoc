#!/usr/bin/env python

from utils import examples, inputs

from sympy import solveset, S
import math


def day06(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    times = []
    distances = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            left, right = line.split(":")
            if left == "Time":
                times.extend(map(int, right.split()))
            if left == "Distance":
                distances.extend(map(int, right.split()))

    from sympy.abc import t

    def ways_to_win(time, distance):
        return len(solveset((time - t) * t > distance, t, domain=S.Integers))

    wins = []
    for time, distance in zip(times, distances):
        wins.append(ways_to_win(time, distance))

    part1 = math.prod(wins)

    # Part2 oh no kerning
    bigtime = int("".join(map(str, times)))
    bigdist = int("".join(map(str, distances)))

    part2 = ways_to_win(bigtime, bigdist)

    print(times, distances, wins)
    print("part1:", part1)
    print("part2:", part2)


day06(examples("06"))
day06(inputs("06"))
