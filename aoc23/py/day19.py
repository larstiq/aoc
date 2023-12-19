#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math


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

    import portion
    ranges = portion.IntervalDict()

    def interp(part):
        for ding in instr:
            ding[ding.rfind(",")] = "|"
            ding.replace
            ding.replace("a", "part['a']").replace(
                    "x", "part['x']"
                    ).replace(
                    "m", "part['m']"
                    ).replace(
                    "s", "part['s']"
                    ).replace(":", "return ").replace(
                            ",", "\n").replace("|", "\nreturn ")

    with open(filename) as puzzlein:
        for line in puzzlein:
            if line.strip() == "":
                continue
            if line[0] != '{':
                workflow, rest = line.strip()[:-1].split("{")
                workflows[workflow] = (rest.split(","))

            else:
                part = eval("dict(" + line.strip()[1:-1] + ")")

                w = "in"
                while w not in ("A", "R"):
                    for instr in workflows[w]:
                        if ':' not in instr:
                            w = instr
                            break
                        rule, target = instr.split(":")

                        assert rule[1] in ("<", ">")
                        component, comp, thres = rule[0], rule[1], rule[2:]

                        if comp == "<":
                            if part[component] < int(thres):
                                w = target
                                break
                        else:
                            if part[component] > int(thres):
                                w = target
                                break

                assert w in ("A", "R")
                if w == "A":
                    accepted.append(part)
                else:
                    rejected.append(part)

    # Ranges
    range_accepted = []
    range_rejected = []
    for (x, m, a, s) in itertools.product(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)):
        part = dict(x=x, m=m, a=a, s=s)
        print(part)
        w = "in"
        while w not in ("A", "R"):
            for instr in workflows[w]:
                if ':' not in instr:
                    w = instr
                    break
                rule, target = instr.split(":")

                assert rule[1] in ("<", ">")
                component, comp, thres = rule[0], rule[1], rule[2:]

                if comp == "<":
                    if part[component] < int(thres):
                        w = target
                        break
                else:
                    if part[component] > int(thres):
                        w = target
                        break

        assert w in ("A", "R")
        if w == "A":
            range_accepted.append(part)
        else:
            range_rejected.append(part)


                

    part1 = sum(sum(part.values()) for part in accepted)
    part2 = len(range_accepted)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day19(examples("19"))
day19(inputs("19"))
