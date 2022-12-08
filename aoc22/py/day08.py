#!/usr/bin/env python

from utils import inputs, examples

from collections import defaultdict

from pathlib import Path

import pandas as pd
import numpy as np


def day08(filename):
    print()
    print(filename)

    sizes = {}
    with open(filename) as puzzlein:


        # TODO shaping

        data = pd.DataFrame(data=[list(map(int, line.strip())) for line in puzzlein])

        visible_trees = set()
        found = data.copy()

        for rowix in range(data.shape[0]):
            for colix in range(data.shape[0]):
                #print(rowix, colix)
                tree = data.loc[rowix][colix]
                from_left = data.loc[rowix][:colix]
                from_right = data.loc[rowix][colix+1:]
                from_top = data[colix][:rowix]
                from_bottom = data[colix][rowix+1:]
                #print(from_left)
                #print(from_right)
                #print(from_top)
                #print(from_bottom)


                if (from_left.max() < tree or 
                    from_right.max() < tree or
                    from_top.max() < tree or
                    from_bottom.max() < tree or rowix == 0 or colix == 0 or rowix == data.shape[0] - 1 or colix == data.shape[1] - 1):
                    #print((rowix, colix), tree)
                        #breakpoint()
                        visible_trees.add((rowix, colix))
                        found.loc[(rowix, colix)] = -100

        print(found)

        print("visible trees:", visible_trees)
        print("len vis:", len(visible_trees))

day08(inputs("08"))
day08(examples("08"))
