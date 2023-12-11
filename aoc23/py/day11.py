#!/usr/bin/env python

from utils import examples, inputs

import pandas as pd
import scipy


def day11(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    data = []

    with open(filename) as puzzlein:
        for line in puzzlein:
            data.append(list(line.strip()))

    df = pd.DataFrame(data)
    expanded_cols = {col for col in df.columns if all(df[col] == '.')}
    expanded_rows = {row for row in df.index if all(df.loc[row] == '.')}

    galaxies = (df[df == '#']).stack().index

    def distances(scale):
        expanded_galaxies = []

        for galaxy in galaxies:
            less_row = {r for r in expanded_rows if r < galaxy[0]}
            less_col = {c for c in expanded_cols if c < galaxy[1]}

            expanded = (
                galaxy[0] + scale * len(less_row),
                galaxy[1] + scale * len(less_col)
                )
            expanded_galaxies.append(expanded)

        pair_distances = scipy.spatial.distance.cdist(expanded_galaxies, expanded_galaxies, metric='cityblock')
        return int(pair_distances.sum() / 2)

    part1 = distances(1)
    part2 = distances(1000000 - 1)
    print("part1:", part1)
    print("part2:", part2)


day11(examples("11"))
day11(inputs("11"))
