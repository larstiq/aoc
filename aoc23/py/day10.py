#!/usr/bin/env python

from utils import examples, inputs

import numpy as np
import pandas as pd
import networkx as nx
import scipy


def day10(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []
    graph = nx.DiGraph()

    with open(filename) as puzzlein:
        for halfrow, line in enumerate(puzzlein):
            row = 2 * halfrow
            data.append(list(line.strip()))
            for halfcolumn, char in enumerate(line.strip()):
                column = 2 * halfcolumn

                graph.add_node((row, column), orig=char)

                # Add neighbouring pipes and pieces inbetween on a doublesize grid
                path = None
                up    = [(row - 2, column), (row - 1, column)]
                down  = [(row + 1, column), (row + 2, column)]
                left  = [(row, column - 2), (row, column - 1)]
                right = [(row, column + 1), (row, column + 2)]
                here = (row, column) 
                if char  == "|":
                    path = up + [here] + down
                elif char == "-":
                    path = left + [here] + right
                elif char == "L":
                    path = up + [here] + right
                elif char == "J":
                    pat = up + [here] + [left[1], left[0]]
                elif char == "7":
                    path = left + [here] + down
                elif char == "F":
                    path = [right[1], right[0]] + [here] + down
                elif char == "S":
                    start = (row, column)

                if path:
                    nx.add_path(graph, path)
                    nx.add_path(graph, reversed(path))


    # What did the starting point connect to?
    neighbours = graph.to_undirected()[start]
    assert len(neighbours) == 2
    for node in neighbours:
        graph.add_edge(start, node)
        diff = node[0] - start[0], node[1] - start[1]
        extended = (node[0] + diff[0], node[1] + diff[1])
        graph.add_edge(node, extended)


    # Find the loop of pipe containing the start
    second = list(graph[start])[0]
    current = second
    seen = set([start, second])

    while current != start:
        followings = set(graph[current]) - seen
        if len(followings) == 0:
            assert current in graph[start]
            break

        following, = followings
        
        seen.add(following)
        current = following

    # We have inserted extra pieces in the pipe so the original halfway point is at a fourth
    part1 = len(seen) // 4

    # Mark all doubled-grid points with original/spliced pipe 
    pijp = np.zeros((2 * len(data), 2 * len(data[0])), dtype=bool)
    for node in seen:
        pijp[node[0]][node[1]] = True

    # Original grid with doubled coordinates
    df = pd.DataFrame(data=data, index=range(0, pijp.shape[0], 2), columns=range(0, pijp.shape[1], 2))
    # Double grid with nans or original data at doubled grid points
    ddf = pd.DataFrame(data=np.nan, index=range(0, pijp.shape[0]), columns=range(0, pijp.shape[1])).combine_first(df)

    # Fill the holes enclosed by the pipe in the doubled grid, and remove the pipe
    inflated = ddf.where(scipy.ndimage.binary_fill_holes(pijp) & ~pijp)
    # Count the number of non-nan entries, this is the number of enclosed original tiles
    part2 = inflated.stack().value_counts().sum()
    print("part1:", part1)
    print("part2:", part2)
    #breakpoint()


day10(examples("10"))
day10(inputs("10"))
day10(examples("10-3"))
