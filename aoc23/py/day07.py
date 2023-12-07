#!/usr/bin/env python

from collections import Counter

from utils import examples, inputs

import itertools

def day07(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    hands = {}
    with open(filename) as puzzlein:
        for line in puzzlein:
            hand, bid = line.strip().split()
            hands[hand] = int(bid)

    mapping = dict(zip(reversed("AKQJT98765432"), itertools.count()))
    def key(c):
        twee = list(reversed(sorted(Counter(c).values())))[:2]
        if len(twee) < 2:
            twee.append(0)
        twee += [mapping[k] for k in c]
        return twee

    mapping2 = dict(zip(reversed("AKQT98765432J"), itertools.count()))
    def key2(c):
        counted = Counter(c)
        if 'J' in counted:
           jcount = counted["J"] 
           del counted["J"]
           if jcount < 5:
               most = counted.most_common()[0][0]
               counted[most] += jcount
           else:
               counted["J"] = jcount

        twee = list(reversed(sorted(counted.values())))[:2]
        if len(twee) < 2:
            twee.append(0)
        twee += [mapping2[k] for k in c]
        return twee
    
    part1 = sum((ix + 1)*hands[hand] for ix, hand in enumerate(sorted(hands, key=key)))
    part2 = sum((ix + 1)*hands[hand] for ix, hand in enumerate(sorted(hands, key=key2)))
    print("part1:", part1)
    print("part2:", part2)
    breakpoint()


day07(examples("07"))
day07(inputs("07"))
