#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx


def day10(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []
    graph = nx.DiGraph()
    with open(filename) as puzzlein:
        for row, line in enumerate(puzzlein):
            data.append(list(line.strip()))
            for column, char in enumerate(line.strip()):
                if char != ".":
                    graph.add_node((row, column))

                if char  == "|":
                    graph.add_edge((row, column), (row - 1, column))
                    graph.add_edge((row, column), (row + 1, column))
                elif char == "-":
                    graph.add_edge((row, column), (row, column - 1))
                    graph.add_edge((row, column), (row, column + 1))
                elif char == "L":
                    graph.add_edge((row, column), (row - 1, column))
                    graph.add_edge((row, column), (row, column + 1))
                elif char == "J":
                    graph.add_edge((row, column), (row - 1, column))
                    graph.add_edge((row, column), (row, column - 1))
                elif char == "7":
                    graph.add_edge((row, column), (row + 1, column))
                    graph.add_edge((row, column), (row, column - 1))
                elif char == "F":
                    graph.add_edge((row, column), (row + 1, column))
                    graph.add_edge((row, column), (row, column + 1))
                #elif char == "S":
                #   graph.add_edge((row, column), (row - 1, column))
                #   graph.add_edge((row, column), (row + 1, column))


    df = pd.DataFrame(data)
    start = df[df == 'S'].stack().index[0]




    #components = [component for component in nx.connected_components(graph) if start in component]
    #for node in components:

    distance = 1
    seen = set([start, (start[0] - 1, start[1]), (start[0] + 1, start[1])])
    current = seen - set([start])

    left
    while True:
        nexts = set()
        for node in current:
            nexts |= set(graph[node])

        nexts -= seen
        if len(nexts) != 2:
            #breakpoint()
            pass
        seen |= nexts
        if len(nexts) == 0:
            print("Current is now", current)
            #breakpoint()
        current = nexts
        distance += 1

        if len(nexts) == 0:
            break
    print(distance)

    #fd = df.copy()
    #for pos in components[0]:
    #    fd[pos[1]][pos[0]] = 'Z'
    import scipy

    aap = np.zeros(df.shape)
    for node in seen:
        aap[node[0]][node[1]] = 1
    
    assert set(df.where(aap == 1).stack().index) == seen
    hrmf = [foo for foo in df.where(scipy.ndimage.binary_fill_holes(aap) != aap).stack().index if foo not in seen]

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


#day10(examples("10"))
day10(inputs("10"))
