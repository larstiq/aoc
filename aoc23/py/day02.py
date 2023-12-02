#!/usr/bin/env python

from utils import inputs, examples

import regex as re

import numpy as np
import pandas as pd



def day02(filename):
    print()
    print(filename)

    games = {}
    maxes = { "red": 12, "green": 13, "blue": 14}
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


    print(games)

    possible = []
    for gid, pull_amounts in games.items():
        nope = False
        for pull in pull_amounts:
            for ball, amount in pull.items():
                if amount > maxes[ball]:
                    nope = True
                    break
            if nope:
                break
        if not nope:
            possible.append(gid)


    print(possible)
    print(sum(possible))

    #print("part1", part1)
    #print("part2", part2)

day02(examples("02"))
day02(inputs("02"))
