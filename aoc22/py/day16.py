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

    max_rate = max(valves.nodes[no]['weight'] for no in valves.nodes)
    #print("max rate:", max_rate)
    #breakpoint()

    for minute in range(1, 26 + 1):
        print("Starting on minute", minute)

        candidates = {}

        for (positions, closed), state in options.items():
            opens = profitable_nodes - closed
            new_pressure = state.pressure + sum(valves.nodes[o]['weight'] for o in opens)
            #print("Minute, pressure", minute, new_pressure)
            #breakpoint()
            #print("New pressure", new_pressure, closed)
            # Is it quicker to just look at the weight?

            if len(positions) == 1:
                you, = elephant, = positions
            else:
                you, elephant = sorted(positions)

            yous = list(valves[you])
            elephants = list(valves[elephant])

            if you in closed:
                yous += [you]
            if elephant in closed and you != elephant:
                elephants += [elephant]

            for next_you in yous:
                for next_elephant in elephants:
                    if (you, elephant) == (next_elephant, next_you):
                        # Swapping places won't help, nor will both opening the same vale help
                        continue

                    new_closed = frozenset(closed)
                    if next_you == you:
                        new_closed = new_closed - {you}
                    if next_elephant == elephant:
                        new_closed = new_closed - {elephant}

                    key = (frozenset({next_you, next_elephant}), new_closed)
                    if len(key[0]) > 2:
                        breakpoint()
                    # Is this taking up too much memory? Let's try without
                    #candidates[key].append(State(new_pressure, state.path + ((minute, key, new_pressure), )))

                    if key in candidates:
                        if candidates[key].pressure < new_pressure:
                            candidates[key] = State(new_pressure, [])
                    else:
                        candidates[key] = State(new_pressure, [])

        #breakpoint()
        options.clear()
        max_state = max(candidates.values())
        max_pressure = max_state.pressure
        options = {opt: state for (opt, state) in candidates.items() if state.pressure + (26 - minute) * max_rate >= max_pressure}


    #print("Best path")
    #print(max(options.values()))
    print("Part2:", max(options.values()).pressure)
    breakpoint()


logging.getLogger().setLevel(logging.WARN)

day16(examples("16"))
day16(inputs("16"))
