#!/usr/bin/env python

import string

from utils import inputs, examples


def day03(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        plays = []
        total = 0
        for line in puzzlein:
            line = line.strip()
            #print(len(line), len(line)/2)
            left, right = line[:len(line)//2], line[len(line)//2:]
            common = set(left).intersection(set(right))
            assert len(common) == 1
            item = common.pop()
            if item in string.ascii_lowercase:
                score = ord(item) - ord('a') + 1
            else:
                score = ord(item) - ord('A') + 27

            print(item, score)
            total += score

        print(total)



day03(inputs("03"))
day03(examples("03"))
