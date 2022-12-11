#!/usr/bin/env python

from utils import inputs, examples

import pandas as pd
import collections
import itertools
import math


class Monkey:

    def __init__(self, items, new, test):
        self.items = items
        self.new = new
        self.test = test
        self.inspect_count = 0

    def inspect(self):
        to_monkies = collections.defaultdict(list)
        for item in self.items:
            self.inspect_count += 1
            new_worry = self.new(item) % (7 * 17 * 11 * 13 * 19 * 2 * 5 * 3)
            #% (23 * 19 * 13 * 17)

            to_monkies[self.test(new_worry)].append(new_worry)

        self.items = []

        return to_monkies

def day11(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0


    monkies = [
        Monkey([79, 98], lambda old: old * 19, lambda item: {True: 2, False: 3}[item % 23 == 0]),
        Monkey([54, 65, 75, 74],
               lambda old:  old + 6,
               lambda item: {True: 2, False: 0}[item % 19 == 0]),
        Monkey([79, 60, 97],
               lambda old:old * old,
               lambda item: 
               {True: 1, False: 3}[item % 13 == 0]),
        Monkey([74], lambda old: old + 3,
               lambda item: 
               {True: 0, False: 1}[item % 17 == 0])
    ]

    import math
    #for m in []:
        #    for n in [23, 19, 13, 17]:
            #    print(m, n, math.gcd(m, n))

    for m in [7, 17, 11, 13, 19, 2, 5, 3]:
        for n in [7, 17, 11, 13, 19, 2, 5, 3]:
            print(m, n, math.gcd(m, n))

    #raise SystemExit


    monkies = [
        Monkey(
            [89, 84, 88, 78, 70],
            lambda old: old * 5,
            lambda item: {True: 6, False: 7}[item % 7 == 0],
        ),
        Monkey(
            [76, 62, 61, 54, 69, 60, 85],
            lambda old: old + 1,
            lambda item: {True: 0, False: 6}[item % 17 == 0],
        ),

        Monkey(
            [83, 89, 53],
            lambda old: old + 8,
            lambda item: {True: 5, False: 3}[item % 11 == 0],
        ),

        Monkey(
            [95, 94, 85, 57],
            lambda old: old + 4,
            lambda item: {True: 0, False: 1}[item % 13 == 0],
        ),

        Monkey(
            [82, 98],
            lambda old: old + 7,
            lambda item: {True: 5, False: 2}[item % 19 == 0],
        ),

        Monkey(
            [69],
            lambda old: old + 2,
            lambda item: {True: 1, False: 3}[item % 2 == 0],
        ),

        Monkey(
            [82, 70, 58, 87, 59, 99, 92, 65],
            lambda old: old * 11,
            lambda item: {True: 7, False: 4}[item % 5 == 0],
        ),

        Monkey(
            [91, 53, 96, 98, 68, 82],
            lambda old: old * old,
            lambda item: {True: 4, False: 2}[item % 3 == 0],
        )
    ]


    for round_ in range(10000):
        for monkey in monkies:
            for target, new_items in monkey.inspect().items():
                monkies[target].items.extend(new_items)


        if round_ % 1000 == 0:
            print()
            print(f"After round {round_}")
            for ix, monkey in enumerate(monkies):
                print(f"Monkey {ix}:", monkey.items)


    print([m.inspect_count for m in monkies])
    print(sorted([m.inspect_count for m in monkies])[-2:])
    #print("part1:", sum(cycle * X for (cycle, X) in signal_strengths if cycle in (20, 60, 100, 140, 180, 220)))
    #print("part2:", part2)


day11(inputs("11"))
day11(examples("11"))
