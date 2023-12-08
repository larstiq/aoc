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
        return  sorted(Counter(c).values(), reverse=True) + [mapping[k] for k in c]

    mapping2 = dict(zip(reversed("AKQT98765432J"), itertools.count()))
    def key2(c):
        counted = Counter(c)
        if "J" in c and c != "JJJJJ":
            counted
        if 'J' in counted:
           jcount = counted["J"] 
           del counted["J"]
           if jcount < 5:
               most = counted.most_common()[0][0]
               counted[most] += jcount
           else:
               counted["J"] = jcount

        twee = list(reversed(sorted(counted.values())))[:2]
        twee += [mapping2[k] for k in c]
        return twee
    
    part1 = sum((ix + 1)*hands[hand] for ix, hand in enumerate(sorted(hands, key=key)))
    part2 = sum((ix + 1)*hands[hand] for ix, hand in enumerate(sorted(hands, key=key2)))

    if str(filename).endswith("inputs/07"):
        assert part1 == 248113761
        assert part2 == 246285222
    else:
        assert part1 == 6440
        assert part2 == 5905

    print("part1:", part1)
    print("part2:", part2)


day07(examples("07"))
day07(inputs("07"))
