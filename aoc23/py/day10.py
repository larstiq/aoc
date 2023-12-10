#!/usr/bin/env python

import math
from collections import Counter, defaultdict, deque

from utils import examples, inputs, display_field

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
                elif char == "S":
                    if str(filename).endswith("inputs/10"):
                       graph.add_edge((row, column), (row - 1, column))
                       graph.add_edge((row, column), (row + 1, column))
                    else:
                       graph.add_edge((row, column), (row, column - 1))
                       graph.add_edge((row, column), (row + 1, column))



    df = pd.DataFrame(data)
    start = df[df == 'S'].stack().index[0]

    #components = [component for component in nx.connected_components(graph) if start in component]
    #for node in components:

    distance = 1
    seen = set([start, (start[0] - 1, start[1]), (start[0] + 1, start[1])])
    seen = set([start, (start[0] - 1, start[1])])

    second = list(graph[start])[0]
    seen = set([start, second])
    current = seen - set([start])

    lefthands = set()


    if second[1] > start[1]:
        direction = 'up'
    elif second[1] < start[1]:
        direction = 'down'
    elif second[0] > start[0]:
        direction = 'left'
    elif second[0] < start[0]:
        direction = 'right'
    else:
        print("WAT")
        breakpoint()

    direction = 'up'


    def left(node, direction):
        if direction == 'left':
            return (node[0] + 1, node[1])
        elif direction == 'right':
            return (node[0] - 1, node[1])
        elif direction == 'up':
            return (node[0], node[1] - 1)
        elif direction == 'down':
            return (node[0], node[1] + 1)

    while True:
        nexts = set()
        for node in current:
            if node not in graph:
                continue
            maybe_left = left(node, direction)
            if maybe_left in graph:
                lefthands.add(maybe_left)
            nexts |= set(graph[node])

        nexts -= seen
        if len(nexts) != 2:
            #breakpoint()
            pass
        seen |= nexts
        if len(nexts) == 0:
            print("Current is now", current)
            #breakpoint()

        if len(nexts) == 0:
            breakpoint()
            break

        assert len(nexts) < 2

        naa = list(nexts)[0]
        naa = df[naa[1]][naa[0]]

        if direction == 'left':
            if naa == '-':
                direction = 'left'
            if naa == 'L':
                direction = 'up'
            if naa == 'F':
                direction = 'down'
        elif direction == 'right':
            if naa == '-':
                direction = 'right'
            if naa == 'J':
                direction = 'up'
            if naa == '7':
                direction = 'down'
        elif direction == 'up':
            if naa == '|':
                direction = 'up'
            if naa == 'F':
                direction = 'right'
            if naa == '7':
                direction = 'left'
        elif direction == 'down':
            if naa == '|':
                direction = 'down'
            if naa == 'L':
                direction = 'right'
            if naa == 'J':
                direction = 'left'
        current = nexts
        distance += 1


    print(distance)
    import scipy


    fd = df.copy()

    aap = np.zeros(df.shape)
    for node in seen:
        aap[node[0]][node[1]] = 1
        fd[node[1]][node[0]] = 'P'
    
    assert set(df.where(aap == 1).stack().index) == seen

    hond = np.zeros(df.shape)
    for node in lefthands:
        if node not in seen:
            hond[node[0]][node[1]] = 1


    mier = np.zeros(df.T.shape)
    for node in (lefthands - seen):
        mier[node[1]][node[0]] = 1

    kameel = np.zeros(df.T.shape)
    for node in seen:
        kameel[node[1]][node[0]] = 1

    display_field(fd.T.where(mier == 1).T)
    display_field(fd.T.where(kameel == 1).T)
    wat = scipy.ndimage.binary_propagation((hond == 1) & (aap == 0), mask=(aap==0))
    huuu = wat & (aap == 0)


    oei = scipy.ndimage.binary_propagation((mier == 1), mask=(kameel == 0))
    display_field(fd.T.where(oei))

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


#day10(examples("10"))
day10(inputs("10"))
#day10(examples("10-3"))
