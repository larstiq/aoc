#!/usr/bin/env python

from utils import inputs, examples


def match_score(opp, you):
    # Loss = 0, Win = 6, draw = 3
    diff = (opp - you) % 3
    if diff == 0:
        return 3
    elif diff == 2:
        return 6
    elif diff == 1:
        return 0


def score(play):
    opp, you = play
    return 1 + you + match_score(opp, you)


def strategy(opp, strategy):
    # (0, 1, 2) = (lose, draw, win)
    if strategy == 1:
        return (opp, opp)
    elif strategy == 0:
        return (opp, (opp + 2) % 3)
    elif strategy == 2:
        return (opp, (opp + 1) % 3)


def day02(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        plays = []
        for line in puzzlein:
            opp, you = line.split()
            play = ord(opp) - ord("A"), ord(you) - ord("X")
            plays.append(play)

        part1 = 0
        part2 = 0
        for play in plays:
            part1 += score(play)
            part2 += score(strategy(*play))

        print("part1:", part1)
        print("part2:", part2)


day02(inputs("02"))
day02(examples("02"))
