#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs, display_field, display_dfield

import numpy as np
import pandas as pd
import networkx as nx
import scipy
import time


def day10(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []
    graph = nx.DiGraph()
    chars = {}

    with open(filename) as puzzlein:
        for halfrow, line in enumerate(puzzlein):
            row = 2 * halfrow
            data.append(list(line.strip()))
            for halfcolumn, char in enumerate(line.strip()):
                column = 2 * halfcolumn

                graph.add_node((row, column), orig=char)
                chars[(row, column)] = char

                if (row, column) == (35, 208):
                    breakpoint()

                # Add neighbouring pipes and pieces inbetween on a doublesize grid
                if char  == "|":
                    graph.add_edge((row,     column), (row - 1, column))
                    graph.add_edge((row - 1, column), (row - 2, column))
                    graph.add_edge((row,     column), (row + 1, column))
                    graph.add_edge((row + 1, column), (row + 2, column))
                elif char == "-":
                    graph.add_edge((row, column    ), (row, column - 1))
                    graph.add_edge((row, column - 1), (row, column - 2))
                    graph.add_edge((row, column    ), (row, column + 1))
                    graph.add_edge((row, column + 1), (row, column + 2))
                elif char == "L":
                    graph.add_edge((row    , column    ), (row - 1, column))
                    graph.add_edge((row - 1, column    ), (row - 2, column))
                    graph.add_edge((row    , column    ), (row, column + 1))
                    graph.add_edge((row    , column + 1), (row, column + 2))
                elif char == "J":
                    graph.add_edge((row,     column    ), (row - 1, column))
                    graph.add_edge((row - 1, column    ), (row - 2, column))
                    graph.add_edge((row,     column    ), (row, column - 1))
                    graph.add_edge((row,     column - 1), (row, column - 2))
                elif char == "7":
                    graph.add_edge((row,     column    ), (row + 1, column))
                    graph.add_edge((row + 1, column    ), (row + 2, column))
                    graph.add_edge((row,     column    ), (row, column - 1))
                    graph.add_edge((row,     column - 1), (row, column - 2))
                elif char == "F":
                    graph.add_edge((row,     column    ), (row + 1, column))
                    graph.add_edge((row + 1, column    ), (row + 2, column))
                    graph.add_edge((row,     column    ), (row, column + 1))
                    graph.add_edge((row,     column + 1), (row, column + 2))
                elif char == "S":
                    start = (row, column)

    neighbours = graph.to_undirected()[start]
    assert len(neighbours) == 2
    for node in neighbours:
        graph.add_edge(start, node)
        diff = node[0] - start[0], node[1] - start[1]
        extended = (node[0] + diff[0], node[1] + diff[1])
        graph.add_edge(node, extended)
        print("Start neighbours", start, node, extended)

    distance = 1
    second = list(graph[start])[0]
    current = second
    seen = set([start, second])

    lefthands = set()
    righthands = set()

    direction = second[0] - start[0], second[1] - start[1]

    def left(node, direction):
        # Left
        if direction == (0, -1):
            return (node[0] + 1, node[1])
        # Right
        elif direction == (0, 1):
            return (node[0] - 1, node[1])
        # Up
        elif direction == (-1, 0):
            return (node[0], node[1] - 1)
        # Down
        elif direction == (1, 0):
            return (node[0], node[1] + 1)

    def right(node, direction):
        if direction == (0, -1):
            return (node[0] - 1, node[1])
        elif direction == (0, 1):
            return (node[0] + 1, node[1])
        elif direction == (-1, 0):
            return (node[0], node[1] + 1)
        elif direction == (1, 0):
            return (node[0], node[1] - 1)


    while True:
        maybe_left = left(current, direction)
        maybe_right = right(current, direction)
        if maybe_left in graph:
            lefthands.add(maybe_left)
        if maybe_right in graph:
            righthands.add(maybe_right)

        nexts = set(graph[current]) - seen
        assert len(nexts) < 2

        if len(nexts) == 0:
            assert start in graph[current]
            break

        nexts = list(nexts)[0]
        seen.add(nexts)

        direction = (nexts[0] - current[0], nexts[1] - current[1])
        current = nexts
        distance += 1

    part1 = len(seen) // 4

    pijp = np.zeros((2 * len(data), 2 * len(data[0])), dtype=bool)
    for node in seen:
        pijp[node[1]][node[0]] = True

    df = pd.DataFrame(data=data, index=range(0, pijp.shape[0], 2), columns=range(0, pijp.shape[1], 2))
    ddf = pd.DataFrame(data=np.nan, index=range(0, pijp.shape[0]), columns=range(0, pijp.shape[1])).combine_first(df)

    #inflated = ddf.where(scipy.ndimage.binary_fill_holes(pijp)).stack().value_counts()
    inflated = ddf.where(scipy.ndimage.binary_fill_holes(pijp)).stack()
    part2 = inflated.loc[~inflated.index.isin(('P', 'M'))].sum()
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


#day10(examples("10"))
day10(inputs("10"))
#day10(examples("10-3"))
