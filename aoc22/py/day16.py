#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools
import networkx as nx



def day16(filename):
    print()
    print(filename)

    valves = nx.Graph()
    with open(filename) as puzzlein:
        for line in puzzlein:
            parts = line.split(" ")
            valves.add_node(parts[1], weight=int(parts[4].split("=")[1].replace(";", "")))
            for neighbour in parts[9:]:
                valves.add_edge(parts[1], neighbour.strip().replace(",", ""))


    # I assume this is not a real digraph in that sense
    #for edge in valves.edges:
        #    assert reversed(edge) in valves.edges

    print(valves.nodes)                                
    print(valves.edges)


    counter = [0]

    def options(current, minutes, pressure, ons, closed):
        if minutes == 30:
            counter[0] += 1
            return [(pressure, minutes, current, tuple(ons))]
        if minutes > 30:
            breakpoint()

        solutions = []

        # TODO: this assumption might be wrong, but if opening a valve and moving to the next chamber both cost 1 minute, is it ever wrong to just open the valve? 
        # Scenarios:
        #    1) open and move, cost 2: , extra pressure is 1 * capacity
        #    2) move, cost 1, extra pressure is 0


        new_ons = ons.copy()
        new_closed = closed.copy()
        new_minutes = minutes
        new_pressure = pressure
        if current in closed:
            new_ons = ons | {current: valves.nodes[current]['weight']}
            new_closed = closed - set([current])
            new_minutes += 1
            new_pressure += sum(new_ons.values())

            if new_minutes == 30:
                counter[0] += 1
                return [(new_pressure, new_minutes, current, tuple(new_ons))]


        #if new_minutes == 29:
            #    breakpoint()
        # We want to relieve pressure, we need to visit closed valves
        for c in new_closed:
            length, path = nx.algorithms.multi_source_dijkstra(valves, {c}, target=current)

            next_minutes = new_minutes
            next_pressure = new_pressure

            # what's the shortest path to get to one of the open nodes?
            for node in reversed(path[:-1]):
                next_minutes += 1
                if next_minutes > 30:
                    break
                next_pressure += sum(new_ons.values())
                if node in new_ons:
                    continue
                else: 
                    solutions.extend(options(node, next_minutes, next_pressure, new_ons, new_closed))
                    break

        if counter[0] % 10000 == 0:
            print(solutions)

        return solutions



    closed = set(n for n in valves.nodes if valves.nodes[n]['weight'] > 0)
    opened = set()

    alles = options('AA', 0, 0, {}, closed)
    breakpoint()


logging.getLogger().setLevel(logging.WARN)

day16(examples("16"))
day16(inputs("16"))
