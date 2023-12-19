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

                

    part1 = sum(sum(part.values()) for part in accepted)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day19(examples("19"))
day19(inputs("19"))
