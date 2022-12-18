#!/usr/bin/env python

import numpy as np
from scipy.ndimage import binary_fill_holes, correlate, generate_binary_structure

from utils import examples, inputs


manhattan_neighbours = generate_binary_structure(3, 1)
manhattan_neighbours[1, 1, 1] = False


def day18(filename):
    print()
    print(filename)

    data = np.loadtxt(filename, delimiter=",", dtype=int).transpose()
    grid = np.zeros(shape=1 + data.max(axis=1), dtype=int)
    grid[data[0], data[1], data[2]] = True

    neighbour_droplets = correlate(grid, manhattan_neighbours, mode="constant", cval=0)
    filled_up = binary_fill_holes(grid, structure=manhattan_neighbours)

    all_surfaces = np.where(grid, 6 - neighbour_droplets, 0).sum()
    interior_surfaces = np.where(filled_up - grid, neighbour_droplets, 0).sum()

    print("part1:", all_surfaces)
    print("part2:", all_surfaces - interior_surfaces)


day18(examples("18"))
day18(inputs("18"))
