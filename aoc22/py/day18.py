#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools

from collections import defaultdict
from dataclasses import dataclass

import time
import scipy



import networkx as nx
import numpy as np
import itertools

def day18(filename):
    print()
    print(filename)

    dimensions = [(0, 0), (0, 0), (0, 0)]
    with open(filename) as puzzlein:
        data = []
        for line in puzzlein:
            droplet = tuple(map(int, line.split(",")))
            data.append(droplet)
            for coordinate in range(3):
                dimensions[coordinate] = min(dimensions[coordinate][0], droplet[coordinate]), max(dimensions[coordinate][1], droplet[coordinate])


    # Check bottom 0
    grid = np.zeros(shape=(dimensions[0][1] + 1, dimensions[1][1] + 1, dimensions[2][1] + 1), dtype=int)

    for droplet in data:
        grid[droplet[0], droplet[1], droplet[2]] = 1


    #for point in np.ndindex(grid.shape):
        #    if grid[point]:
            #surroundings = grid[point[0] - 1:point[0] + 1, point[1] - 1:point[1] + 1, point[2] - 1, point[2] + 1]
            #print(point)
    
    #numpy.array(
    #connections = nx.Graph()
    #for droplet in data:
    #    connections.add_node(droplet)


    neighbours = np.array([[[False, False, False],
                         [False,  True, False],
                         [False, False, False]],

                        [[False,  True, False],
                         [ True, False,  True],
                         [False,  True, False]],

                        [[False, False, False],
                         [False,  True, False],
                         [False, False, False]]])



    connected = scipy.ndimage.correlate(grid, neighbours, mode='constant', cval=0)


    sides = 0
    for point in np.ndindex(grid.shape):
        if grid[point]:
            #breakpoint()
            this_sides = 6 - connected[point]
            sides += this_sides
            print(point, this_sides, sides)


    print("part1:", sides)


    #print(data)

    breakpoint()






logging.getLogger().setLevel(logging.WARN)

day18(examples("18"))
day18(inputs("18"))
