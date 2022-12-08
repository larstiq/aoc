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





        max_scenic = 0

        print(data)
        # Can avoid the edges since they count anyway
        # TODO: combine both by being visible from a high vantage point
        for rowix in range(data.shape[0]):
            for colix in range(data.shape[0]):
                tree = data.loc[rowix][colix]
                from_left = data.loc[rowix][:colix]
                from_right = data.loc[rowix][colix+1:]
                from_top = data[colix][:rowix]
                from_bottom = data[colix][rowix+1:]
                print((rowix, colix), tree)



                max_left = -1
                left_scenic = 0
                right_scenic = 0
                top_scenic = 0
                bottom_scenic = 0
                for t in reversed(from_left):
                    left_scenic += 1 
                    if t >= tree:
                        break
                for t in from_right:
                    right_scenic += 1 
                    if t >= tree:
                        break
                for t in reversed(from_top):
                    top_scenic += 1 
                    if t >= tree:
                        break
                for t in from_bottom:
                    bottom_scenic += 1 
                    if t >= tree:
                        break

                scenic = left_scenic * right_scenic * top_scenic * bottom_scenic
                if scenic > max_scenic:
                    max_scenic = scenic

                    # Don't care about multiple trees, so stop at first? Need to flip things then
                assert len(from_left) + len(from_right) == data.shape[0] - 1
                assert len(from_top) + len(from_bottom) == data.shape[0] - 1

                if not (list(from_left) + [tree] + list(from_right) == list(data.loc[rowix])
                        and list(from_top) + [tree] + list(from_bottom) == list(data[colix])):
                    breakpoint()
                #assert from_left
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

        print("max scenic:", max_scenic)
        print(found)
        breakpoint()

        print("visible trees:", visible_trees)
        print("len vis:", len(visible_trees))

day08(inputs("10"))
day08(examples("08"))
