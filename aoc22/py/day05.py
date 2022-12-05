#!/usr/bin/env python

from utils import inputs, examples

import copy
from pprint import pprint


def day05(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:

        part1 = 0
        part2 = 0
        for line in puzzlein:
            instructions =[]
            for line in puzzlein:
                if line.startswith("move"):
                    parts = line.split(" ")
                    instructions.append(tuple(map(int, (parts[1], parts[3], parts[5]))))

        print(str(filename))
        if "examples" in str(filename):
            stacks = {
                1: ['Z', 'N'],
                2: ['M', 'C', 'D'],
                3: ['P']
            }
        else:
            stacks = {
                1: list(reversed(list("VQWMBNZC"))),
                2: list(reversed(list("BCWRZH"))),
                3: list(reversed(list("JRQF"))),
                4: list(reversed("T M N F H W S Z".split(" "))),
                5: list(reversed("P Q N L W F G".split())),
                6: list(reversed("W P L".split())),
                7: list(reversed("J Q C G R D B V".split())),
                8: list(reversed("W B N Q Z".split())),
                9: list(reversed("J T G C F L H".split())),
            }


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
