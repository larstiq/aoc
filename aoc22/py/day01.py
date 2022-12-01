#!/usr/bin/env python

from utils import inputs, examples


def day01(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        elves = []
        elf = 0
        for line in puzzlein:
            if line == "\n":
                elves.append(elf)
                elf = 0
            else:
                elf += int(line.strip())

        if elf > 0:
            elves.append(elf)

    print("part1", max(elves))
    print("part2", sum(sorted(elves)[-3:]))


day01(examples("01"))
day01(inputs("01"))
