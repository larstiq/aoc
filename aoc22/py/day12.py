#!/usr/bin/env python

from utils import inputs, examples

import collections
import copy
import logging
import math

import sympy

import pandas as pd

import numpy as np
import string
import networkx
import itertools


def day12(filename):
    print()
    print(filename)



    data = []
    start = None
    dingen = 'S' + string.ascii_lowercase + 'E'
    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(list(line.strip()))

    df = pd.DataFrame(data)
    print(df)
    # TODO: might need to adjust to a and z
    print(df == 0) # start
    #breakpoint()
    # print(df == len(dingen) - 1) end

    graph = networkx.DiGraph()

    start = None
    end = None
    for idx in np.ndindex(df.shape):
        node = df.loc[idx[0]][idx[1]]
        if node == "S":
            start = idx
        if node == "E":
            end = idx
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neigh_idx = idx[0] + direction[0], idx[1] + direction[1]
            try:
                neighbour = df.loc[neigh_idx[0]][neigh_idx[1]]
            except KeyError: continue

            #if len({idx, neigh_idx}.intersection({(2, 5), (3, 6)})) > 0:
                #    breakpoint()

            if node == "S":
                node = "a"
            elif node == "E":
                node = "z"

            if neighbour == "S":
                neighbour = "a"
            elif neighbour == "E":
                neighbour = "z"

            #if ord(neighbour) in (ord(node) + 1, ord(node)):
            if ord(neighbour) <= ord(node) + 1:
                print(node, neighbour)
                graph.add_edge(idx, (idx[0] + direction[0], idx[1] + direction[1]))


    #print(len(list(networkx.all_shortest_paths(graph, start, end))[0]))
    steps = df.copy()
    #breakpoint()
    for pair in pairwise(networkx.shortest_path(graph, start, end)):
        if pair[0][0] < pair[1][0]:
            steps.loc[pair[0][0]][pair[0][1]] = 'v'
        elif pair[0][0] > pair[1][0]:
            steps.loc[pair[0][0]][pair[0][1]] = '^'
        elif pair[0][1] < pair[1][1]:
            steps.loc[pair[0][0]][pair[0][1]] = '>'
        elif pair[0][1] > pair[1][1]:
            steps.loc[pair[0][0]][pair[0][1]] = '<'

    print(steps)
    #breakpoint()
    print(graph)


    print(len(networkx.shortest_path(graph, start, end)))

    coord = (df == 'a').stack()
    coord[coord == False] = np.nan

    opts = []
    for s in coord.dropna().index:
        try:
            opts.append(len(networkx.shortest_path(graph, s, end)))
        except:
            pass

    print(opts)
    print(min(opts))
    breakpoint()
    

            
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
                







logging.getLogger().setLevel(logging.DEBUG)

day12(examples("12"))
day12(inputs("12"))
