#!/usr/bin/env python

from utils import inputs, examples

import copy
from pprint import pprint

from collections import defaultdict
import string


def day05(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:

        stacks = defaultdict(list)
        instructions = []
        for line in puzzlein:
            if line.startswith("move"):
                parts = line.split(" ")
                instructions.append(tuple(map(int, (parts[1], parts[3], parts[5]))))
            else:
                for ix, crate in enumerate(range(1, len(line), 4)):
                    crate = line[crate]
                    if crate in string.ascii_uppercase:
                        stacks[1 + ix].insert(0, crate)

        part1 = copy.deepcopy(stacks)
        part2 = copy.deepcopy(stacks)

        for instr in instructions:
            amount, source, dest = instr
            temp = []
            for i in range(amount):
                temp.append(part2[source].pop())
                part1[dest].append(part1[source].pop())

            part2[dest].extend(reversed(temp))
            pprint(part1)
            pprint(part2)

        print(instructions)
        pprint(part1)
        pprint(part2)

        print("part1:", "".join(part1[i][-1] for i in range(1, 1 + len(stacks))))
        print("part1:", "".join(part2[i][-1] for i in range(1, 1 + len(stacks))))


day05(inputs("05"))
day05(examples("05"))
