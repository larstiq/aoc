#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict

import re

def day19(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        data = [list(map(int, re.findall("\d+", line))) for line in puzzlein]




    # We can rewrite how much a geode costs in resources

    #Blueprint 1:
    #  Each ore robot costs 4 ore.
    #  Each clay robot costs 2 ore.
    #  Each obsidian robot costs 3 ore and 14 clay.
    #  Each geode robot costs 2 ore and 7 obsidian.
    #
    # -> geode = 2 ore + 7 obsidian
    #          = 2 ore + 7 * (3 ore and 14 clay)
    #          = 23 ore + 14*2 ore
    #          = 51 ore
    #
    # So at a minimum we need to have produced 51 ore to get a geode
    #
    # Will it be faster to construct another clay robot or just wait to make an obsidian one?
    #
    # I guess we just have to try all choices

    qualities = []
    mgeodes = []
    for recipe in data:
        bid, ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = recipe
        states = { (1, 0, 0, 0): [[0, 0, 0, 0]] }
        max_geode = -1
        for minute in range(1, 24 + 1):
            minutes_left = 24 - minute
            print("Minute", minute, "for", bid, "starting with", sum(len(v) for v in states.values()), "states")

            next_states = defaultdict(list)

            for (robots, resources_list) in states.items():
                for resources in resources_list:

                    possible_choices = [0, 0, 0, 0]
                    # TODO: is it faster to construct more clay robots or more obsidian robots?
                    # TODO: munge input data to have uniform comparison in resource cost
                    if resources[0] >= geode_ore and resources[2] >= geode_obsidian:
                        possible_choices[3] = 1
                    if resources[0] >= obsidian_ore and resources[1] >= obsidian_clay:
                        possible_choices[2] = 1
                    if resources[0] >= clay:
                        possible_choices[1] = 1
                    if resources[0] >= ore:
                        possible_choices[0] = 1


                    for ix, v in enumerate(possible_choices):
                        if v:
                            next_resources = resources.copy()

                            for jx, V in enumerate(robots):
                                next_resources[jx] += V

                            next_robots = list(robots)
                            next_robots[ix] += 1

                            if ix == 3:
                                next_resources[0] -= geode_ore
                                next_resources[2] -= geode_obsidian
                            elif ix == 2:
                                next_resources[0] -= obsidian_ore
                                next_resources[1] -= obsidian_clay
                            elif ix == 1:
                                next_resources[0] -= clay
                            elif ix == 0:
                                next_resources[0] -= ore
                            
                            if next_resources[-1] > max_geode:
                                max_geode = next_resources[-1]

                            if max_geode - next_resources[-1] > minutes_left * next_resources[-1] + (minutes_left + 1)*minutes_left / 2:
                                #print("Skipping", next_resources, "since", max_geode, "unbeatable at", minute)
                                continue

                                
                            cands = next_states[tuple(next_robots)] 
                            for other_resources in cands:
                                # If there is the same amount of robots but with less resources,
                                # don't keep that state
                                if (next_resources[0] <= other_resources[0] and 
                                   next_resources[1] <= other_resources[1] and 
                                   next_resources[2] <= other_resources[2] and 
                                   next_resources[3] <= other_resources[3]):
                                    break
                            else:
                                next_states[tuple(next_robots)].append(next_resources)
                                
                    # Or, do nothing
                    next_resources = resources.copy()

                    if next_resources[-1] > max_geode:
                        max_geode = next_resources[-1]

                    for jx, V in enumerate(robots):
                        next_resources[jx] += V
                    next_states[robots].append(next_resources)

            
            states = next_states

                
        ql = bid * max_geode
        qualities.append(ql)
        mgeodes.append(max_geode)
        print("quality level for", bid, ql, max_geode)

    
    print(data)
    print("part1:", sum(qualities))
    print("part2:", mgeodes[0] * mgeodes[1] * mgeodes[2])
    breakpoint()


day19(examples("19"))
day19(inputs("19"))
