#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

TURNS = {
    UP: [LEFT, RIGHT],
    DOWN: [RIGHT, LEFT],
    LEFT: [UP, DOWN],
    RIGHT: [
        DOWN,
        UP,
    ],
}

DIGS = {
    "U": UP,
    "D": DOWN,
    "R": RIGHT,
    "L": LEFT,
    0: RIGHT,
    1: DOWN,
    2: LEFT,
    3: UP,
}

def day18(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(line.strip())

    df = pd.DataFrame(data)

    dug = pd.DataFrame(data=False, index=range(-2000, 2000), columns=range(-2000, 2000))

    start = (0, 0)
    pos = start
    dug[0][0] = True

    corners = [start]
    boundary = 1

    area = 0
    x = 0
    y = 0
    distances = []
    for instructions in data:
        letter, amount, colour = instructions.split()
        amount = int(amount)
        direction = DIGS[letter]
        for step in range(1, amount + 1):
            pos = pos[0] + direction[0], pos[1] + direction[1]
            dug[pos[1]][pos[0]] = True


        # Part2
        distance = int(colour[2:-2], 16)
        direction = DIGS[int(colour[-2])]
        #pos = pos[0] + (distance) * direction[0], pos[1] + (distance) * direction[1]

        prevcorner = corners[-1]
        amount_or_distance = distance
        distances.append(distance)
        corner = prevcorner[0] + (amount_or_distance + 0) * direction[0], prevcorner[1] + (amount_or_distance + 0) * direction[1]
        corners.append(corner)
        dx = amount_or_distance * direction[0]
        dy = amount_or_distance * direction[1]
        #area += (x * 2 + dx)*dy

        area += y*(x + dx) - x*(y + dy) 
        x += dx
        y += dy
        boundary += amount_or_distance


    # Close the loop with the start
    print(distances)
    assert corners[-1] == start



    print("manual:", area, area/2, area + boundary//2 - 1)
    import shapely
    vertices = np.array(corners)
    polygon = shapely.Polygon(corners)
    print("shapely:", polygon.buffer(0.5, join_style='mitre').area)

    def shoelace(x_y):
        x_y = np.array(x_y)
        x_y = x_y.reshape(-1,2)

        x = x_y[:,0]
        y = x_y[:,1]

        S1 = np.sum(x*np.roll(y,-1))
        S2 = np.sum(y*np.roll(x,-1))

        area = .5*np.absolute(S1 - S2)

        return area

    def polygon_area(vertices):
        """
        Return the area of the polygon enclosed by vertices using the shoelace
        algorithm.

        """

        a = np.vstack((vertices, vertices[0]))
        S1 = sum(a[:-1,0] * a[1:,1])
        S2 = sum(a[:-1,1] * a[1:,0])
        return abs(S1-S2)/2
            
    print(corners)

    interior = polygon_area(corners)
    pick = interior + (boundary + 1)/2
    print(shoelace(corners))
    print("pick:", pick)



    #print(dug)
    DUG = scipy.ndimage.binary_fill_holes(dug)
    part1 = DUG.sum().sum()
        

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day18(examples("18"))
day18(inputs("18"))
