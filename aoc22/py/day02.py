#!/usr/bin/env python

from utils import inputs, examples


def score(opp, you):
    # Rock
    # Paper
    # Scissors

    if opp == you:
        return 3
    if opp == 1:   # Opp rock
        if you == 3: # YOu scissors, lose
            return 0
        if you == 2: # Paper win
            return 6
    if opp == 2: # Opp paper
        if you == 3: # You scicorrs
            return 6
        if you == 1: # YOu rock
            return 0

    if opp == 3: #Scirros
        if you == 2: #  beats paper
            return 0
        if you == 1: # loses to paper
            return 6


def strat(opp, strategy):
    # 1: you need to lose
    # 2: you need draw
    # 3: you need to win
    if strategy == 2:
        return (opp, opp)
    if strategy == 1:
        if opp == 1:
            return (opp, 3)
        if opp == 2:
            return (opp, 1)
        if opp == 3:
            return (opp, 2)
    if strategy == 3:
        if opp == 1:
            return (opp, 2)
        if opp == 2:
            return (opp, 3)
        if opp == 3:
            return (opp, 1)
    

def day02(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        plays = []
        for line in puzzlein:
            opp, you = line.split()
            play = 1 + ord(opp) - ord('A'), 1 + ord(you) - ord('X')
            plays.append(strat(*play))
            print(play)

        print(plays)
        total = 0
        for play in plays:
            total += play[1] + score(*play)

        print("part1", total)
    #print("part2", sum(sorted(elves)[-3:]))


day02(inputs("02"))
day02(examples("02"))
