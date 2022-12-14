#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools

import pandas as pd

def day14(filename):
    print()
    print(filename)

    part1 = part2 = 0
    data = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append([list(map(int, coord.split(","))) for coord in line.strip().split(" -> ")])

    min_x = min(min(path[0] for path in paths) for paths in data)
    max_x = max(max(path[0] for path in paths) for paths in data)

    min_y = min(min(path[1] for path in paths) for paths in data)
    max_y = max(max(path[1] for path in paths) for paths in data)

    #breakpoint()
    print((min_x, max_x), (min_y, max_y))
    print(data)


    # Sand coming in from 500,0
    cave = pd.DataFrame(data='.', columns=range(min_x, max_x + 1), index=range(min(0, min_y), max_y + 1))
    print(cave)


    for paths in data:
        for (start, end) in more_itertools.pairwise(paths):
            print("Looking at", start, end)
            if start[0] == end[0]:
                for ix in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                    cave[start[0]][ix] = '#'
            elif start[1] == end[1]:
                for ix in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    cave[ix][start[1]] = '#'
            else:
                print("Cornerncase")
                breakpoint()


    # TODO: copy cave with rock

    #print(cave)


    # SIMULATE
    on_the_map = True
    import itertools
    for sand in itertools.count():
        current_sand = (500, 0)
        while True:
            try:
                if cave[current_sand[0]][current_sand[1] + 1] == '.': 
                    current_sand = current_sand[0], current_sand[1] + 1
                # TODO: handle going off border
                elif cave[current_sand[0] - 1][current_sand[1] + 1] == '.': 
                    current_sand = current_sand[0] - 1, current_sand[1] + 1
                elif cave[current_sand[0] + 1][current_sand[1] + 1] == '.': 
                    current_sand = current_sand[0] + 1, current_sand[1] + 1
                else:
                    # This should mean we hit sand or rock, let's check
                    cave[current_sand[0]][current_sand[1]] = '+'
                    #print(cave)
                    #breakpoint()
                    break
            except KeyError:
                on_the_map = False
                break
        if not on_the_map:
            break

    print("part1:", sand)


    print("part2:", part2)


logging.getLogger().setLevel(logging.WARN)

day14(examples("14"))
day14(inputs("14"))
