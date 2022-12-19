#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict
import time

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
    start_time = time.time()
    for recipe in data[:3]:
        bid, ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = recipe
        states = { (1, 0, 0, 0): {(0, 0, 0, 0)} }
        max_geode = -1
        for minute in range(1, 32 + 1):
            prev_max = max_geode
            minutes_left = 32 - minute
            print("Minute", minute, "for", bid, "starting with", sum(len(v) for v in states.values()), f"states over {len(states)} robots", time.time() - start_time)

            next_states = defaultdict(set)

            for (robots, resources_list) in states.items():
                for resources in resources_list:

                    # We can always not build a robot
                    possible_choices = [(0, 0, 0, 0)] 
                    # TODO: is it faster to construct more clay robots or more obsidian robots?
                    # TODO: munge input data to have uniform comparison in resource cost
                    if resources[0] >= geode_ore and resources[2] >= geode_obsidian:
                        possible_choices.append((0, 0, 0, 1))
                    if resources[0] >= obsidian_ore and resources[1] >= obsidian_clay:
                        possible_choices.append((0, 0, 1, 0))
                    if resources[0] >= clay:
                        possible_choices.append((0, 1, 0, 0))
                    if resources[0] >= ore:
                        possible_choices.append((1, 0, 0, 0))

                    for choice in possible_choices:
                        next_resources = list(resources)
                        next_robots = list(robots)

                        for jx, V in enumerate(robots):
                            next_resources[jx] += V
                            next_robots[jx] += choice[jx]

                        if choice == (0, 0, 0, 1):
                            next_resources[0] -= geode_ore
                            next_resources[2] -= geode_obsidian
                        elif choice == (0, 0, 1, 0):
                            next_resources[0] -= obsidian_ore
                            next_resources[1] -= obsidian_clay
                        elif choice == (0, 1, 0, 0):
                            next_resources[0] -= clay
                        elif choice == (1, 0, 0, 0):
                            next_resources[0] -= ore

                        max_geode = max(max_geode, next_resources[-1])

                        next_states[tuple(next_robots)].add(tuple(next_resources))


            print("Starting pruning", time.time() - start_time)

            if minute == 31:
                max_last_geodes = -1
                cand = None
                for (robots, resources) in next_states.items():
                    for rx in resources:
                        if rx[-1] + robots[-1] > max_last_geodes:
                            cand = (robots, rx)
                            max_last_geodes = rx[-1] + robots[-1]

                print("Last minute:", max_last_geodes, cand)
                breakpoint()
                    
            # TODO: if either robots or resources are the same as another option, can take the lexically greatest option
            #
            #       Basically we're looking at a surface in (robot, resource) space. 
            state_to_robot = defaultdict(set)
            im_states = defaultdict(set)

            if len(next_states) == 1:
                print(next_states)


            pruned_resources = 0
            pruned_on_geodes = 0
            for next_robots in next_states:
                cands = sorted(next_states[next_robots])

                for ix, next_resources in enumerate(cands):
                    state_to_robot[next_resources].add(next_robots)

                    if max_geode - next_resources[-1] > minutes_left * next_resources[-1] + (minutes_left + 1)*minutes_left / 2:
                        pruned_on_geodes += 1
                        #print("Skipping", next_resources, "since", max_geode, "unbeatable at", minute)
                        continue

                    for other_resources in cands[ix + 1:]:
                        #breakpoint()
                        # If there is the same amount of robots but with less resources,
                        # don't keep that state
                        if (next_resources[0] > other_resources[0] or 
                           next_resources[1] > other_resources[1] or 
                           next_resources[2] > other_resources[2] or 
                           next_resources[3] > other_resources[3]):
                            continue
                        else:
                            pruned_resources += 1
                            break
                    else:
                        im_states[next_robots].add(next_resources)

            print(f"   pruned {pruned_on_geodes} on geodes, {max_geode} max", time.time() - start_time)
            print(f"   pruned {pruned_resources} resources", time.time() - start_time)

            states = defaultdict(set)
            #all_resources = sum(len(v) for v in states.values())
            #import functools
            #dedup_resources = len(functools.reduce(lambda x, y: x | set(y), states.values(), set()))
            #if all_resources != dedup_resources:
            #    print(all_resources - dedup_resources)
            #    breakpoint()

            pruned_robots = 0
            for state, robots_set in state_to_robot.items():
                robots_list = sorted(robots_set)
                for jx, r1 in enumerate(robots_list):
                    for r2 in robots_list[jx + 1:]:
                        if (
                            r1[0] > r2[0] or 
                            r1[1] > r2[1] or 
                            r1[2] > r2[2] or 
                            r1[3] > r2[3]
                        ):
                            r1[0] - r2[0], r1[1] - r2[1], r1[2] - r2[2], r1[3] - r2[3]
                            
                            continue
                        else:
                            pruned_robots += 1
                            break
                    else:
                        if state in im_states[r1]:
                            states[r1].add(state)

            print(f"   pruned {pruned_robots} robots", time.time() - start_time)

        ql = bid * max_geode
        qualities.append(ql)
        mgeodes.append(max_geode)
        print("quality level for", bid, ql, max_geode)

    
    print(data)
    print("part1:", sum(qualities))
    print("part2:", mgeodes[0] * mgeodes[1] * mgeodes[2])
    breakpoint()


day19(examples("19"))
#day19(inputs("19"))
