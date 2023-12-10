#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs, display_field, display_dfield

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
        for row, line in enumerate(puzzlein):
            data.append(list(line.strip()))
            for column, char in enumerate(line.strip()):
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

    df = pd.DataFrame(data)

    import itertools
    # Maybe arange or shift with 0.5 or something

    ddf = pd.DataFrame(data=np.nan, columns=np.arange(0, df.columns[-1] + .5, .5), index=np.arange(0, df.index[-1] + .5, .5)).combine_first(df).fillna('M')


    start = df[df == 'S'].stack().index[0]

    neighbours = graph.to_undirected()[start]
    assert len(neighbours) == 2
    for node in neighbours:
        graph.add_edge(start, node)

    distance = 1
    second = list(graph[start])[0]
    seen = set([start, second])
    current = second

    lefthands = set()
    righthands = set()

    direction = second[0] - start[0], second[1] - second[0]

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


    traversal = np.zeros(df.shape, dtype=bool)
    traversal[start[0]][start[1]] = True
    import time
    while True:
        maybe_left = left(current, direction)
        maybe_right = right(current, direction)
        if maybe_left in graph:
            lefthands.add(maybe_left)
        if maybe_right in graph:
            righthands.add(maybe_right)
        traversal[current[0]][current[1]] = True

        #if len(seen) > 12000:
        #    display_dfield(
        #            df.where(traversal).dropna(how='all').dropna(how='all', axis='columns')
        #    )
        #    time.sleep(0.0001)
        #print(f"Nexts for {current}: {nexts} pipelenght {len(seen)}")

        nexts = set()
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

    print("Maak")
    for edge in graph.edges(seen):
        mid = (edge[0][0] + edge[1][0])/2, (edge[0][1] + edge[1][1])/ 2
        ddf[mid[1]][mid[0]] = 'P'
    print("Klaar")

    
    fd = df.copy()

    aap = np.zeros(df.shape, dtype=bool)
    for node in seen:
        aap[node[0]][node[1]] = True
        ddf[node[1]][node[0]] = 'P'

    pijp = ddf == 'P'
    
    assert set(df.where(aap == 1).stack().index) == seen

    hond = np.zeros(df.shape, dtype=bool)
    for node in lefthands:
        if node not in seen:
            hond[node[0]][node[1]] = True

    kat = np.zeros(df.shape, dtype=bool)
    for node in righthands:
        if node not in seen:
            kat[node[0]][node[1]] = True


    wat = scipy.ndimage.binary_propagation(hond & ~aap, mask=~aap)
    taw = scipy.ndimage.binary_propagation(kat & ~aap, mask=~aap)

    buis_plus_binnen = scipy.ndimage.binary_fill_holes(aap)
    echt_recht = buis_plus_binnen & taw 
    echt_links = buis_plus_binnen & wat
    groot_recht = scipy.ndimage.binary_fill_holes(echt_recht) & ~aap
    groot_links = scipy.ndimage.binary_fill_holes(echt_links) & ~aap

    part1 = math.ceil((len(seen) - 1) / 2)
    inflated = ddf.where(scipy.ndimage.binary_fill_holes(pijp)).stack().value_counts()
    part2 = inflated.loc[~inflated.index.isin(('P', 'M'))].sum()
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


#day10(examples("10"))
day10(inputs("10"))
#day10(examples("10-3"))
