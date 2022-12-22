#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict, deque
import time

import numpy as np
import re

import networkx as nx
import sympy

from dataclasses import dataclass


def day22(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    password = None


    mapping = {
        " ": 0,
        ".": 1,
        "#": 2,
    }

    raw_board = []
    with open(filename) as puzzlein:
        for line in puzzlein:
            if set(line).issubset(set(".# \n")):
                raw_board.append([mapping[c] for c in line if c != "\n"])
            else:
                password = line


    max_width = max(len(l) for l in raw_board)
    height = len(raw_board)

    board = np.zeros(shape=(height, max_width), dtype=int)
    for row, line in enumerate(raw_board):
        for col, car in enumerate(raw_board[row]):
            board[row, col] = car

    print(board)

    # Direction, 
    # 0 right
    # 1 down
    # 2 left
    # 3 up

    moves = []
    if password == "10R5L5R10L4R5L5\n":
        moves = [(10, 'R'), 
                 (5, "L"),
                 (5, "R"),
                 (10, "L"),
                 (4, "R"),
                 (5, "L"),
                 (5, "N")
                ]
    else:
        breakpoint()
        ps = 0
        pe = 0
        while pe < len(password.strip()):
            if password[pe] in "LR":
                moves.append((int(password[ps:pe]), password[pe]))
                ps = pe + 1
                pe += 2
            else:
                pe += 1


    if moves[-1] == (14, 'R'):
        moves.append((39, 'N'))


    # Find first 1 in first row
    position = [0, 8]
    direction = 0
    for move in moves:
        distance, turn = move
        
        for i in range(distance):
            stepped = False
            forwards = position.copy()

            while not stepped:
                if direction == 0:
                    forwards[1] += 1
                elif direction == 1:
                    forwards[0] += 1
                elif direction == 2:
                    forwards[1] -= 1
                elif direction == 3:
                    forwards[0] -= 1


                if forwards[0] == -1:
                    forwards[0] = board.shape[0] - 1
                elif forwards[1] == -1:
                    forwards[1] = board.shape[1] - 1

                try:
                    next_square = board[forwards[0], forwards[1]]
                except IndexError:
                    # wrap around
                    if direction == 0:
                        forwards[1] = 0
                    elif direction == 1:
                        forwards[0] = 0
                    elif direction == 2:
                        forwards[1] = board.shape[1] - 1
                    elif direction == 3:
                        forwards[0] = board.shape[0] - 1

                    next_square = board[forwards[0], forwards[1]]
                    
                if next_square == 1:
                    stepped = True
                    position = forwards
                    print("Stepped into", position, direction)
                elif next_square == 2:
                    stepped = True

        if turn == "R":
            direction = (direction + 1) % 4
        if turn == "L":
            direction = (direction - 1) % 4

        print("Facing", direction)
                


    #print(board, password)
    breakpoint()
    print(position, direction)

    part1 = 1000 * (position[0] + 1) + 4 * (position[1] + 1) + direction

    print("part1:", part1)
    print("part2:", part2)


day22(examples("22"))
day22(inputs("22"))
