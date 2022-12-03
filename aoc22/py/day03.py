#!/usr/bin/env python

import string

from utils import inputs, examples


def score(item):
    if item in string.ascii_lowercase:
        score = ord(item) - ord('a') + 1
    else:
        score = ord(item) - ord('A') + 27

    return score


def day03(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        plays = []
        total = 0
        group = []
        badges = 0
        for line in puzzlein:
            line = line.strip()
            #print(len(line), len(line)/2)
            left, right = line[:len(line)//2], line[len(line)//2:]
            common = set(left).intersection(set(right))
            assert len(common) == 1
            item = common.pop()
            total += score(item)

            group.append(set(line))
            if len(group) == 3:
                badge = group[0].intersection(group[1]).intersection(group[2]).pop()
                badges += score(badge)
                print(badge, badges)
                group = []


        print(total)
        print(badges)



day03(inputs("03"))
day03(examples("03"))
