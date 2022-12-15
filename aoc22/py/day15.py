#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools

import pandas as pd

def day15(filename):
    print()
    print(filename)

    sensors = []
    beacons = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            s, b = line.split(":")
            sensors.append(tuple(map(lambda x: int(x.split("=")[1]), s.split(","))))
            beacons.append(tuple(map(lambda x: int(x.split("=")[1]), b.split(","))))


    distances = []
    for ix, (sensor, beacon) in enumerate(zip(sensors, beacons)):
        d = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        distances.append(d)


    min_x = min(min(s[0] for s in sensors), min(b[0] for b in beacons))
    max_x = max(max(s[0] for s in sensors), max(b[0] for b in beacons))

    min_y = min(min(s[1] for s in sensors), min(b[1] for b in beacons))
    max_y = max(max(s[1] for s in sensors), max(b[1] for b in beacons))

    print(sensors)
    print(beacons)

    # Example, y = 10
    # What are the ys that can be reached?


    covered_by_sensor = set()
    row = 2000000
    for ix, s in enumerate(sensors):
        print()
        print("Looking at sensor", ix, s)
        #y_d = abs(s[1] - 2000000)
        y_d = abs(s[1] - row)

        max_d = distances[ix]
        print("Distances", y_d, "<?", max_d)
        if y_d < max_d:
            max_x_d = max_d - y_d
            print("  and thus", max_x_d)
            #breakpoint()

            covered_by_sensor |= set((x, row) for x in range(s[0] - max_x_d, s[0] + max_x_d + 1))


    print('cover')

    no_beacon = covered_by_sensor.difference(set(beacons)).difference(set(sensors))
    #print(no_bea
    print("part1:", len(no_beacon))
    breakpoint()


logging.getLogger().setLevel(logging.WARN)

#day15(examples("15"))
day15(inputs("15"))
