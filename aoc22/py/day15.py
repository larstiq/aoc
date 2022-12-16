#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools

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
    row = 10
    max_row = min(max(max_x, max_y), 4000000)

    beacons_s = set(beacons)
    sensors_s = set(sensors)
    sensors_or_beacons = beacons_s | sensors_s


    for x in range(0, max_row + 1):
        intersections = []
        for ix, s in enumerate(sensors):
            max_d = distances[ix]
            # TODO: sort the balls so can skip linearly through

            # We fall within the sensor
            if abs(x - s[0]) < max_d:
                # At this level of x, which bits of y do we get?
                # We are within the sensor ball, skip to the next we need to check
                max_y = max_d - abs(x - s[0])
                
                intersections.append((s[1] - max_y, s[1] + max_y))

        intersections.sort()


        # We know we're sorted
        def combine(p1, p2):
            return min(p1[0], p2[0]), max(p1[1], p2[1])

        current = None
        collapsed = []
        current = intersections[0]
        for interval in intersections:
            if current[1] + 1 < interval[0]:
                collapsed.append(current)
                current = interval
            else:
                current = combine(current, interval)

        collapsed.append(current)
        if len(collapsed) > 1:
            print("part2:", x * 4000000 + collapsed[0][1] + 1)

logging.getLogger().setLevel(logging.WARN)

day15(examples("15"))
day15(inputs("15"))
