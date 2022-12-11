#!/usr/bin/env python

from utils import inputs, examples

import collections
import copy
import logging
import math

import sympy


old = sympy.symbols("old")


class Monkey:
    def __init__(self, items, worry, divisor, test):
        self.items = items
        self.divisor = divisor
        self.worry = worry
        self.test = test
        self.inspect_count = 0

    def inspect(self, divisors):
        to_monkies = collections.defaultdict(list)
        for item in self.items:
            self.inspect_count += 1
            new_worry = self.worry(item)

            if divisors == 1:
                new_worry //= 3
            else:
                new_worry %= divisors

            to_monkies[self.test[new_worry % self.divisor == 0]].append(new_worry)

        self.items = []

        return to_monkies

    def __str__(self):
        return f"Monkey: {self.items} worries {self.worry} by {self.divisor} to {self.test}"

    def __repr__(self):
        return str(self)


def day11(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:

        chunks = puzzlein.read().split("Monkey ")

    monkies = []
    for c in chunks:
        if c == "":
            continue
        for line in c.split("\n"):
            line = line.strip()
            if line.startswith("Starting items: "):
                items = [int(getal.strip()) for getal in line.split(":")[1].split(",")]
            elif line.startswith("Operation: "):
                new_worry = sympy.lambdify(
                    old, sympy.parse_expr(line.split("=")[1].strip())
                )
            elif line.startswith("Test: "):
                divisor = int(line.split("by")[1].strip())
            elif line.startswith("If true:"):
                truemonkey = int(line.split()[-1])
            elif line.startswith("If false:"):
                falsemonkey = int(line.split()[-1])

        monkies.append(
            Monkey(items, new_worry, divisor, {True: truemonkey, False: falsemonkey})
        )

    logging.debug(monkies)
    part1(copy.deepcopy(monkies))
    part2(copy.deepcopy(monkies))


def score(monkies):
    top_two = sorted([m.inspect_count for m in monkies])[-2:]
    business = math.prod(top_two)

    logging.debug("Monkey inspect counts: %s", [m.inspect_count for m in monkies])
    logging.debug("  top two: %s", top_two)
    logging.debug("  monkey business: %s", business)

    return business


def part1(monkies):
    for round_ in range(20):
        for monkey in monkies:
            for target, new_items in monkey.inspect(1).items():
                monkies[target].items.extend(new_items)

    print("part1:", score(monkies))


def part2(monkies):
    part2_divisors = math.prod(m.divisor for m in monkies)

    for round_ in range(10000):
        for monkey in monkies:
            for target, new_items in monkey.inspect(part2_divisors).items():
                monkies[target].items.extend(new_items)

        if round_ % 1000 == 0:
            logging.debug("")
            logging.debug(f"After round {round_}")
            for ix, monkey in enumerate(monkies):
                logging.debug(f"Monkey {ix}: %s", monkey.items)

    print("part2:", score(monkies))


logging.getLogger().setLevel(logging.WARN)

day11(inputs("11"))
day11(examples("11"))
