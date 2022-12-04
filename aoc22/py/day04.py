#!/usr/bin/env python

from utils import inputs, examples


def section_to_set(section):
    start, end = map(int, section.split("-"))
    return set(range(start, end + 1))

def day04(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:

        part1 = 0
        part2 = 0
        for line in puzzlein:
            left, right = map(section_to_set, line.strip().split(","))

            if left.issubset(right) or right.issubset(left):
                part1 += 1
            if len(left.intersection(right)) > 0:
                part2 += 1

        print("part1:", part1)
        print("part1:", part2)


day04(inputs("04"))
day04(examples("04"))
