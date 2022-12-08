#!/usr/bin/env python

from utils import inputs, examples

import pandas as pd


def day08(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        # TODO shaping
        data = pd.DataFrame(data=[list(map(int, line.strip())) for line in puzzlein])

        visible_trees = set()
        found = data.copy()

        # TODO: avoid the edges since they are trivial
        # TODO: combine part1 and part2 by viewing from outside

        max_scenic = 0
        for rowix in range(data.shape[0]):
            for colix in range(data.shape[0]):
                tree = data.loc[rowix][colix]
                from_left = data.loc[rowix][:colix][::-1]
                from_right = data.loc[rowix][colix+1:]
                from_top = data[colix][:rowix][::-1]
                from_bottom = data[colix][rowix+1:]

                if (from_left.max() < tree or 
                    from_right.max() < tree or
                    from_top.max() < tree or
                    from_bottom.max() < tree or rowix == 0 or colix == 0 or rowix == data.shape[0] - 1 or colix == data.shape[1] - 1):
                        visible_trees.add((rowix, colix))
                        found.loc[(rowix, colix)] = -100

                scenic = 1
                for sightline in (from_left, from_right, from_top, from_bottom):
                    partial_scenic = 0
                    for t in sightline:
                        partial_scenic += 1 
                        if t >= tree:
                            break
                    scenic *= partial_scenic

                if scenic > max_scenic:
                    max_scenic = scenic


        print("part1 visible trees from outside:", len(visible_trees))
        print("part2 max scenic view:", max_scenic)

day08(inputs("08"))
day08(examples("08"))
