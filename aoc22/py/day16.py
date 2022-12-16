#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools
import networkx as nx

from collections import defaultdict
from dataclasses import dataclass

@dataclass
class State:
    pressure: int
    path: tuple[str]

    def __lt__(self, other):
        return self.pressure < other.pressure


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


    #part1(closed, valves, profitable_nodes)
    part2(closed, valves, profitable_nodes)



def part1(closed, valves, profitable_nodes):
    options = {("AA", frozenset(closed)): State(0, ())}

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


    #print("Best path")
    #:w
    #print(max(options.values()))
    print("Part1:", max(options.values()).pressure)
    #:w
    #breakpoint()


def part2(closed, valves, profitable_nodes):
    # Now we have a helperfant so we need to track two positions
    options = {(frozenset(["AA"]), frozenset(closed)): State(0, ())}

    for minute in range(1, 26 + 1):
        print("Starting on minute", minute)

        candidates = defaultdict(list)

        for (positions, closed), state in options.items():
            opens = profitable_nodes - closed
            new_pressure = state.pressure + sum(valves.nodes[o]['weight'] for o in opens)
            #print("Minute, pressure", minute, new_pressure)
            #breakpoint()
            #print("New pressure", new_pressure, closed)
            # Is it quicker to just look at the weight?

            if len(positions) == 1:
                current = ecurrent = list(positions)[0]
            else:
                current, ecurrent = list(positions)

            if current in closed:
                if ecurrent in closed:
                    # Both opening
                    key = frozenset({current, ecurrent}), closed - { current, ecurrent}
                    if len(key[0]) == 0:
                        breakpoint()
                    candidates[key].append(State(new_pressure, state.path + ((minute, (current, ecurrent), new_pressure),)))
                else:
                    # You opening
                    for neighbour in valves[ecurrent]:
                        key = frozenset({current, neighbour}), closed
                        if len(key[0]) == 0:
                            breakpoint()
                        candidates[key].append(State(new_pressure, state.path + ((minute, (current, neighbour), new_pressure), )))
            else:
                if ecurrent in closed:
                    # Elephant opening
                    for neighbour in valves[current]:
                        key = frozenset({neighbour, ecurrent}), closed - {ecurrent}
                        if len(key[0]) == 0:
                            breakpoint()
                        candidates[key].append(State(new_pressure, state.path + ((minute, (neighbour, ecurrent), new_pressure), )))
                else:
                    for neighbour in valves[current]:
                        for eneighbour in valves[ecurrent]:
                            key = frozenset({neighbour, eneighbour}), closed
                            if len(key[0]) == 0:
                                breakpoint()
                            candidates[key].append(State(new_pressure, state.path + ((minute, (neighbour, eneighbour), new_pressure), )))

        #breakpoint()
        options.clear()
        options = {opt: max(states) for opt, states in candidates.items()}
        print(max(options.values()))


    #print("Best path")
    #print(max(options.values()))
    print("Part2:", max(options.values()).pressure)
    breakpoint()


logging.getLogger().setLevel(logging.WARN)

day16(examples("16"))
#day16(inputs("16"))
