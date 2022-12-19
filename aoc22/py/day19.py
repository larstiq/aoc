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

    for recipe in data:
        bid, ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = recipe
        states = { ((0, 0, 0, 0), (1, 0, 0, 0)) }
        qualities = []
        for minute in range(1, 24 + 1):
            print("Minute", minute, "for", bid)

            next_states = defaultdict(list)
            max_geode = -1

            for (resources, robots) in states:

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
                        next_resources = list(resources)

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

                        next_states[tuple(next_resources), tuple(next_robots)].append((resources, robots))
                    

                # Or, do nothing
                next_resources = list(resources)

                if next_resources[-1] > max_geode:
                    max_geode = next_resources[-1]

                for jx, V in enumerate(robots):
                    next_resources[jx] += V
                next_states[tuple(next_resources), robots].append((resources, robots))
                    

            
            max_states = defaultdict(list)
            for (rx, ro) in next_states:
                max_states[ro].append(rx)


            # If there is the same amount of robots but with less resources,
            # don't keep that state
            states = set()

            for ro, res in max_states.items():
                for rx in res:
                    alts = sum([rx[0] <= ro[0] and rx[1] <= ro[1] and rx[2] <= ro[2] and rx[3] <= ro[3] for ro in res])
                    if alts > 1:
                        # There is another set of resources with the same robot
                        # that has more of at least one resource and no less of the rest
                        # so we can ignore this one
                        continue

                    minutes_left = 24 - minute

                    # At a rate of one robot per minute, the most we can add is
                    #   minutes_left * robots + sum(1, minutes_left)
                    #   minutes_left * robots + (minutes_left + 1)*minutes_left / 2
                    if max_geode - rx[-1] > minutes_left * rx[-1] + (minutes_left + 1)*minutes_left / 2:
                        continue

                    states.add((rx, ro))
                        #print("Found an alternative")
                
                
        max_geodes = -1
        for s in states:
            if s[0][-1] > max_geodes:
                max_geodes =  s[0][-1]

        ql = bid * max_geodes
        qualities.append(ql)
        print("quality level for", bid, ql, max_geodes)

    
    print(data)
    print("part1:", sum(qualities))
    breakpoint()
    print("part2:", part2)


day19(examples("19"))
#day19(inputs("19"))
