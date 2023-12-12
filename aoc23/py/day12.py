#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math
import re
import exrex


def day12(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    equal = 0
    unequal = 0
    solved = []
    unsolved = []
    parts = {}

    grandcounts = []
    replacings = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            breakpoint()
            springs, counts = line.split()
            springs = "?".join(5 * [springs])
            counts = ",".join(5 * [counts])
            counts = counts.split(",")
            kounts = list(map(int, counts))

            expanded = "0".join("1" * int(leng) for leng in counts) 

            #if "." in springs:
            #    knowns = [piece for piece in springs.split(".") if piece != '']
            #else:
            #    knowns = springs


            replaced = "0".join(piece for piece in springs.replace("#", '1').split(".") if piece != "")
            # Regexify
            replaced = replaced.replace("?", "(0|1){0,1}")


            simpler = "^" + line.replace("?", "(_|-){0,1}") + "$"


            preugh = "0".join(piece for piece in springs.replace("#", '1').split(".") if piece != "")


            nuu = Counter(preugh)
            tot = Counter(expanded)
            missing = tot['1'] - nuu['1']
            


            options = []
            # would it be faster per peice? eh
            for ix in range(2**sum(c not in '01' for c in preugh)):
                # We need exactly two bits set, can skip the rest of the number.
                # Should this just be combinations of powers of 2?
                # Could pick all combinations of size k amon what?
                possible_replacement = bin(ix + 2**40)[-nuu['?']:]
                if Counter(possible_replacement)['1'] != missing:
                    continue

                ugh = preugh
                it = iter(possible_replacement)
                while "?" in ugh:
                    ugh = ugh.replace("?", next(it), 1)

                #print(ugh)
                subcounts = [str(sum(1 for _ in group)) for label, group in itertools.groupby(ugh) if label == '1']

                if subcounts == counts:
                    options.append(ugh)


            print(line, options, len(options))
            grandcounts.append(len(options))


    part1 = sum(grandcounts)
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day12(examples("12"))
day12(inputs("12"))
