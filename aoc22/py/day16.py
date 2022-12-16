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

    valves = nx.DiGraph()
    with open(filename) as puzzlein:
        for line in puzzlein:
            parts = line.split(" ")
            valves.add_node(parts[1], weight=int(parts[4].split("=")[1].replace(";", "")))
            for neighbour in parts[9:]:
                valves.add_edge(parts[1], neighbour.strip().replace(",", ""))

    print(valves.nodes)                                
    print(valves.edges)
    breakpoint()



    def options(current, path, minutes, pressure, ons):
        if minutes == 30:
            print(minutes, path)
            return [(pressure, tuple(path), tuple(ons))]


        solutions = []
        for neighbour in valves[current]:
            try:
                prev = path[-2] 
                if prev == neighbour:
                    # Avoid cycles
                    continue
            except IndexError:
                pass
            solutions.extend(options(neighbour, path + [neighbour], minutes + 1, pressure + sum(ons.values()), ons))

        if current not in ons:
            new_ons = ons | {current: valves.nodes[current]['weight']}
            solutions.extend(options(current, path + [current], minutes + 1, pressure + sum(new_ons.values()), new_ons))

        return solutions


    alles = options('AA', ['AA'], 0, 0, {})
    breakpoint()


logging.getLogger().setLevel(logging.WARN)

day16(examples("16"))
day16(inputs("16"))
