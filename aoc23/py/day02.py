#!/usr/bin/env python

from utils import inputs, examples

from collections import Counter
from math import prod


def day02(filename):
    print()
    print(filename)

    games = {}
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            left, right = line.split(":")
            gid = int(left.split(" ")[1])

            pulls = right.split(";")
            pull_amounts = []
            for pull in pulls:
                ball_amounts = Counter()
                balls = pull.split(",")
                for ball in balls:
                    amount, colour = ball.strip().split(" ")
                    ball_amounts[colour] = int(amount)

                pull_amounts.append(ball_amounts)

            games[gid] = pull_amounts


    maxes = Counter(red=12, green=13, blue=14)
    possible_games = set()
    game_powers = []
    for gid, pull_amounts in games.items():
        minimum = Counter()
        for pull in pull_amounts:
            minimum |= pull

        if minimum < maxes:
            possible_games.add(gid)

        game_powers.append(prod(minimum.values()))


    part1 = sum(possible_games)
    part2 = sum(game_powers)

    if str(filename).endswith("inputs/02"):
        assert part1 == 2265
        assert part2 == 64097

    print("part1", part1)
    print("part2", part2)


day02(examples("02"))
day02(inputs("02"))
