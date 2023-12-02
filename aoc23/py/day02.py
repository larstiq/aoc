#!/usr/bin/env python

from utils import inputs, examples

from collections import Counter


def day02(filename):
    print()
    print(filename)

    games = {}
    maxes = Counter({ "red": 12, "green": 13, "blue": 14})
    with open(filename) as puzzlein:
        for line in puzzlein:
            line = line.strip()
            left, right = line.split(":")
            gid = int(left.split(" ")[1])

            pulls = right.split(";")
            pull_amounts = []
            for pull in pulls:
                ball_amounts = {}
                balls = pull.split(",")
                for ball in balls:
                    amount, colour = ball.strip().split(" ")
                    ball_amounts[colour] = int(amount)

                pull_amounts.append(ball_amounts)

            games[gid] = pull_amounts


    possible_games = []
    powers = []
    for gid, pull_amounts in games.items():
        nope = False
        minus = Counter({"red": 0, "blue": 0, "green": 0})
        for pull in pull_amounts:
            for ball, amount in pull.items():
                if amount > minus[ball]:
                    minus[ball] = amount
                if amount > maxes[ball]:
                    nope = True
        if not nope:
            possible_games.append(gid)

        mv = list(minus.values())
        powers.append(mv[0] * mv[1] * mv[2])


    part1 = sum(possible_games)
    part2 = sum(powers)

    print("part1", part1)
    print("part2", part2)


day02(examples("02"))
day02(inputs("02"))
