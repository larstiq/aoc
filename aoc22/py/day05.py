#!/usr/bin/env python

from utils import inputs, examples


def day04(filename):
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

        import pprint
        pprint.pprint(stacks)

        for instr in instructions:
            amount, source, dest = instr
            for i in range(amount):
                stacks[dest].append(stacks[source].pop())


        print(stacks)
        for stack in range(1, 10):
            print(stacks[stack][-1])


        print(instructions)


        print("part1:", part1)
        print("part1:", part2)


day04(inputs("05"))
day04(examples("05"))
