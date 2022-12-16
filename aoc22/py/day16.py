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

    profitable_nodes = set(n for n in valves.nodes if valves.nodes[n]['weight'] > 0)
    closed = profitable_nodes.copy()
    opened = set()




    # What state do we need to keep track of?
    # If at minute M we are currently at node A, and nodes O are open, then we
    # don't care how we got here we just go with the highest pressure option
    # since that represents the best way of having gotten here.
    #
    # So the key should be (current, open) and the value should be pressure
    #
    # Also storing the 

    from dataclasses import dataclass

    @dataclass
    class State:
        pressure: int
        path: tuple[str]

        def __lt__(self, other):
            return self.pressure < other.pressure

    options = {("AA", frozenset(closed)): State(0, ())}

    from collections import defaultdict
    for minute in range(1, 30 + 1):
        print("Starting on minute", minute)

        candidates = defaultdict(list)

        for (current, closed), state in options.items():
            opens = profitable_nodes - closed
            new_pressure = state.pressure + sum(valves.nodes[o]['weight'] for o in opens)
            #print("New pressure", new_pressure, closed)
            # Is it quicker to just look at the weight?
            if current in closed:
                candidates[(current, closed - { current } )].append(State(new_pressure, state.path + ((minute, current, new_pressure),)))

            for neighbour in valves[current]:
                candidates[(neighbour, closed)].append(State(new_pressure, state.path + ((minute, neighbour, new_pressure), )))

        #breakpoint()
        options.clear()
        options = {opt: max(states) for opt, states in candidates.items()}
        print(max(options.values()))


    print("Best path")
    print(max(options.values()))
    breakpoint()



logging.getLogger().setLevel(logging.WARN)

day16(examples("16"))
day16(inputs("16"))
