#!/usr/bin/env python

from collections import defaultdict
from utils import examples, inputs


def HASH(s):
    current = 0
    for char in s:
        current += ord(char)
        current *= 17
        current %= 256
    return current


def day15(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    commands = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            commands.extend(line.strip().split(","))

    hashes = []
    focal_lengths = {}
    boxes = defaultdict(list)
    for part in commands:
        if "=" in part:
            label, action, focus = part.partition("=")
        else:
            label, action, _ = part.partition("-")

        box = HASH(label)
        if action == "-":
            if label in boxes[box]:
                boxes[box].remove(label)
        elif action == "=":
            if label not in boxes[box]:
                boxes[box].append(label)

            focal_lengths[label] = int(focus)

        hashes.append(HASH(part))

    part1 = sum(hashes)

    part2 = 0
    for boxid, lenses in boxes.items():
        focusing_power = [
            (1 + boxid) * (ix + 1) * focal_lengths[label]
            for (ix, label) in enumerate(lenses)
        ]
        part2 += sum(focusing_power)

    print("part1:", part1)
    print("part2:", part2)


day15(examples("15"))
day15(inputs("15"))
