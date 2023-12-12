#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from utils import examples, inputs

import pandas as pd
import scipy
import numpy as np
import networkx as nx
import itertools
import math


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

    with open(filename) as puzzlein:
        for line in puzzlein:
            grandcount = 1
            springs, counts = line.split()

            if "." in springs:
                knowns = [piece for piece in springs.split(".") if piece != '']
            else:
                knowns = springs

            unmatched = counts
            matched = []

            for pp in knowns:
                if pp in parts:
                    options = parts[pp]
                else:
                    if all(x == "#" for x in pp):
                        options = [str(len(pp))]
                    else:
                        options = []
                        aap = pp.replace('#', '1')
                        preaap = []
                        import string
                        for rep, orig in zip(string.ascii_letters, aap):
                            chois = orig if orig == '1' else rep
                            preaap.append(chois)

                        postaap = ''.join(preaap)

                        for ix in range(2**sum(c == '?' for c in pp)):
                            hond = bin(2**40 + ix)[-len(pp):]

                            replacements = dict(zip([ch for ch in postaap if ch != '1'], hond))

                            prereplaced = []
                            for ch in postaap:
                                if ch == '1':
                                    prereplaced.append(ch)
                                else:
                                    prereplaced.append(replacements[ch])

                            postreplaced = ''.join(prereplaced)

                            subcounts = [str(sum(1 for _ in group)) for label, group in itertools.groupby('0001101')]
                            options.append(subcounts)

                    parts[pp] = options

                piececount = 0
                for opt in options:
                    if counts.startswith(alt + ",".join(opt)):



    print(equal, unequal)
    df = pd.DataFrame(data)

    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day12(examples("12"))
day12(inputs("12"))
