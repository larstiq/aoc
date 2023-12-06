#!/usr/bin/env python

from utils import examples, inputs

from sympy import solve, integrate
from math import ceil, floor, prod

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


    from sympy.abc import t, T, N
    race_win_boundaries = solve((T - t)*t - N, t)

    def ways_to_win(time, distance):
        concrete = dict(T=time, N=distance)
        exact_lower = race_win_boundaries[0].subs(concrete).evalf()
        exact_upper = race_win_boundaries[1].subs(concrete).evalf()
        # When the solution is exactly an integer we need to step 1 away to beat the score
        lower = int(exact_lower + 1) if exact_lower % 1 == 0 else ceil(exact_lower)
        upper = int(exact_upper - 1) if exact_upper % 1 == 0 else floor(exact_upper)
        return 1 + upper - lower


    wins = []
    for time, distance in zip(times, distances):
        wins.append(ways_to_win(time, distance))

    part1 = prod(wins)

    # Part2
    bigtime = int("".join(map(str, times)))
    bigdist = int("".join(map(str, distances)))

    part2 = 1 + floor(race_win_boundaries[1].subs(dict(T=bigtime, N=bigdist))) -  ceil(race_win_boundaries[0].subs(dict(T=bigtime, N=bigdist)))


    print(times, distances, wins)
    print("part1:", part1)
    print("part2:", part2)


day06(examples("06"))
day06(inputs("06"))
