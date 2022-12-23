#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict, deque, Counter
import time

import numpy as np
import re
import itertools

import networkx as nx
import sympy

from dataclasses import dataclass
from scipy.ndimage import binary_fill_holes, correlate, generate_binary_structure


def display_grove(grove):
    for line in grove:
        print("".join("#" if g else "." for g in line))

def day23(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(line.strip())

    # Enough of a border that in 10 rounds we won't hit it:w

    grove = np.zeros(shape=(len(data)+80, len(data[0])+80), dtype=int)

    for ix, line in enumerate(data):
        for jx, lc in enumerate(line):
            if lc == "#":
                grove[80+ix, 80+jx] = 1
            
    print(grove)


    neighbours = generate_binary_structure(2, 2)
    neighbours[1, 1] = 0

    south = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [1, 1, 1],
    ])
    north = np.array([
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0],
    ])
    west = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
    ])
    east = np.array([
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
    ])


    global_mms = [[None, None], [None, None]]

    for round_ in itertools.count():
        elves = np.where(grove)
        # Order of moves:
        #   
        # 1 North
        # 2 South
        # 3 West
        # 4 East

        # TODO: might need cval=1
        count_elves = correlate(grove, neighbours, mode="constant", cval=0)
        unhappy_elves = np.where(count_elves > 0, grove, 0)

        free_north = correlate(grove, north, mode="constant", cval=0) == 0
        free_south = correlate(grove, south, mode="constant", cval=0) == 0
        free_west  = correlate(grove, west,  mode="constant", cval=0) == 0
        free_east  = correlate(grove, east,  mode="constant", cval=0) == 0

        northerlings = unhappy_elves * free_north
        southerlings = unhappy_elves * free_south
        westerlings  = unhappy_elves * free_west
        easterlings  = unhappy_elves * free_east

        # TODO: cycle the directions

        unhappy_coords = np.where(unhappy_elves)
        directions = deque([(northerlings, (-1, 0)), (southerlings, (1, 0)), (westerlings, (0, -1)), 
                            (easterlings, (0, 1))])
        directions.rotate(-round_)


        # How to execute the move
        suggestions = defaultdict(list)
        for elf in zip(unhappy_coords[0], unhappy_coords[1]):
            for richting, vec in directions:
                if richting[elf[0], elf[1]]:
                    suggestions[elf[0] + vec[0], elf[1] + vec[1]].append(elf)
                    break
            else:
                suggestions[elf].append(elf)

        #breakpoint()
        new_grove = np.where(count_elves == 0, grove, 0)
        for suggestion, hopefuls in suggestions.items():
            if len(hopefuls) == 1:
                new_grove[suggestion[0], suggestion[1]] = 1
            else:
                for elf in hopefuls:
                    new_grove[elf[0], elf[1]] = 1

        print(f"At the end of round {round_} the grove looks like")
        #display_grove(new_grove)

        mm_elves = np.where(new_grove)

        if global_mms[0][0] is None or min(mm_elves[0]) < global_mms[0][0]:
            global_mms[0][0] = min(mm_elves[0])
        if global_mms[0][1] is None or max(mm_elves[0]) > global_mms[0][1]:
            global_mms[0][1] = max(mm_elves[0])
        if global_mms[1][0] is None or min(mm_elves[1]) < global_mms[1][0]:
            global_mms[1][0] = min(mm_elves[0])
        if global_mms[1][1] is None or max(mm_elves[1]) > global_mms[1][1]:
            global_mms[1][1] = max(mm_elves[1])


        if (grove == new_grove).all():
            part2 = round_ + 1
            break

        grove = new_grove
            
        
    print(global_mms)
    end_elves = np.where(new_grove)
    min_rect = new_grove[min(end_elves[0]):max(end_elves[0])+1, min(end_elves[1]):max(end_elves[1])+1]
    part1 = (min_rect == 0).sum(axis=None)

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


#day23(examples("23-1"))
day23(examples("23"))
day23(inputs("23"))
