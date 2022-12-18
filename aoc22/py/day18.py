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


    neighbours = np.array(
        [[[False, False, False],
          [False,  True, False],
          [False, False, False]],

         [[False,  True, False],
          [ True, False,  True],
          [False,  True, False]],

         [[False, False, False],
          [False,  True, False],
          [False, False, False]]])


    neighdexes = np.array([
        ( 0,  0, -1),
        ( 0, -1,  0),
        (-1 , 0,  0),
        ( 0,  0,  1),
        ( 0,  1,  0),
        ( 1 , 0,  0),
    ])



    connected = scipy.ndimage.correlate(grid, neighbours, mode='constant', cval=0)


    sides = 0
    for point in np.ndindex(grid.shape):
        if grid[point]:
            #breakpoint()
            this_sides = 6 - connected[point]
            sides += this_sides
            print(point, this_sides, sides)


    print("part1:", sides)

    exterior = 0

    filled_up = scipy.ndimage.binary_fill_holes(grid, structure=neighbours)

    #exterior = sides - 6 * (filled_up - grid).sum()
    exterior = sides
    #filled_connected = scipy.ndimage.correlate(filled_up, neighbours, mode='constant', cval=0)
    for point in np.ndindex(grid.shape):
        if (filled_up - grid)[point]:
            #print(point)
            #:w
            #breakpoint()

            for direc in neighdexes:
                if grid[point[0] + direc[0], point[1] + direc[1], point[2] + direc[2]]:
                    exterior -= 1
            #for neighp in neighdexes + point:
                #    print(grid[*neighp])
            
            #    #breakpoint()
            #this_sides = 6 - filled_connected[point]
            #exterior += this_sides
            #print(point, this_sides, exterior)

    print("part2:", exterior)

    #print(data)

    breakpoint()






logging.getLogger().setLevel(logging.WARN)

day18(examples("18"))
day18(inputs("18"))
