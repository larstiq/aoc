#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math
from heapq import heappop, heappush


def day19(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []


    accepted = []
    rejected = []
    workflows = {"A": lambda part: accepted.append(part),
                "R": lambda part: rejected.append(part)
                }
    workflows = {}

    import portion
    ranges = portion.IntervalDict()


    terms = Counter()
    with open(filename) as puzzlein:
        for line in puzzlein:
            if line.strip() == "":
                continue
            if line[0] != '{':
                workflow, rest = line.strip()[:-1].split("{")
                wfls = rest.split(",")
                workflows[workflow] = wfls[:-2] + [wfls[-2] + "," + wfls[-1]]
                print(workflows[workflow])
                terms[workflow] += 1

                for instr in rest.split(","):
                    if ':' in instr:
                        rule, target = instr.split(":")
                        terms[target] += 1
                    else:
                        terms[instr] += 1

            else:
                continue
                part = eval("dict(" + line.strip()[1:-1] + ")")

                w = "in"
                while w not in ("A", "R"):
                    for instr in workflows[w]:
                        rule, target = instr.split(":")

                        assert rule[1] in ("<", ">")
                        component, comp, thres = rule[0], rule[1], rule[2:]

                        if comp == "<":
                            if part[component] < int(thres):
                                w = target
                        else:
                            if part[component] > int(thres):
                                w = target

                assert w in ("A", "R")
                if w == "A":
                    accepted.append(part)
                else:
                    rejected.append(part)

    # Assumption, the instructions encode a tree, each instruction is only targeted once
    # We can walk through the list of instructions refining the tree and then
    # pick the next unhandled leaf
    for (term, freq) in terms.items():
        if freq > 2:
            assert term in ("R", "A")

    components = "xmsa"


    boom = defaultdict(list)
    boom["in"].append({component: range(1, 4000 + 1) for component in components})
    unhandled = set(workflows.keys())
    handled = set()
    discovered = set(["in"])

    while discovered:
        # Disjoint union, slow check but soit
        assert (handled | unhandled) == set(workflows.keys())
        assert handled.intersection(unhandled) == set()

        node = discovered.pop()
        handled.add(node)
        unhandled -= {node}

        childer = boom[node]

        outerblock = childer[0]
        block = outerblock

        for instruction in workflows[node]:
            rule, target = instruction.split(":")
            assert rule[1] in ("<", ">")
            component, comp, thres = rule[0], rule[1], rule[2:]
            thres = int(thres)
            final = None

            if "," in target:
                target, final = target.split(",")
                childer.append(final)
                if final not in ("A", "R"):
                    discovered.add(final)

            childer.append(target)
            if target not in ("A", "R"):
                discovered.add(target)

            if comp == "<":
                left =  block | {component: range(block[component].start, thres)}
                right = block | {component: range(thres, block[component].stop)}

                boom[target].append(left)
                block = right
                if final is not None:
                    boom[final].append(block)

            elif comp == ">":
                left =  block | {component: range(block[component].start, thres + 1)}
                right = block | {component: range(thres + 1, block[component].stop)}

                boom[target].append(right)
                block = left
                if final is not None:
                    boom[final].append(block)


    part1 = sum(sum(part.values()) for part in accepted)

    accepted = [len(block['x']) * len(block['a']) * len(block['m']) * len(block['s']) for block in boom['A']]
    rejected = [len(block['x']) * len(block['a']) * len(block['m']) * len(block['s']) for block in boom['R']]
    part2 = sum(accepted)
    print("accepted:", sum(accepted))
    print("rejected:", sum(rejected))
    print("hmm:", sum(accepted) + sum(rejected) - 4000**4)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day19(examples("19"))
day19(inputs("19"))
