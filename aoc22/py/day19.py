#!/usr/bin/env python

from utils import examples, inputs


import re

def day19(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        data = [list(map(int, re.findall("\d+", line))) for line in puzzlein]


    robots = {bid: [1, 0, 0, 0] for bid in range(1, len(data) + 1)}
    resources = {bid: [0, 0, 0, 0] for bid in range(1, len(data) + 1)}

    for minute in range(1, 24 + 1):
        for recipe in data:
            bid, ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = recipe

            this_resources = resources[bid]
            this_robots = robots[bid]

            # TODO: is it faster to construct more clay robots or more obsidian robots?
            if this_resources[0] > geode_ore and this_resources[2] > geode_obsidian:
                this_resources[0] -= geode_ore
                this_resources[2] -= geode_obsidian
                this_robots[2] += 1
            elif this_resources[0] > obsidian_ore and this_resources[1] > obsidian_clay:
                this_resources[0] -= obsidian_ore
                this_resources[1] -= obsidian_clay
                this_robots[2] += 1
            elif this_resources[0] > clay:
                this_resources[0] -= clay
                this_robots[1] += 1
            elif this_resources[0] > ore:
                this_resources[0] -= ore
                this_robots[0] += 1
            
            for ix, _ in enumerate(this_resources):
                this_resources[ix] += this_robots[ix]
            #print(this_resources)
            print(this_robots)

    print(data)
    breakpoint()
    print("part1:", part1)
    print("part2:", part2)


day19(examples("19"))
day19(inputs("19"))
