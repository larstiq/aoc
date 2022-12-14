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
    revmapping = {
        0: " ",
        1: ".",
        2: "#",
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

    # Surround with a zero-border to avoid index-errors
    board = np.zeros(shape=(height + 2, max_width + 2), dtype=int)
    pathboard = np.zeros(shape=(height + 2, max_width + 2), dtype=str)
    for row, line in enumerate(raw_board):
        for col, car in enumerate(raw_board[row]):
            board[row + 1, col + 1] = car
            pathboard[row + 1, col + 1] = revmapping[car]

    print(board)

    # Direction, 
    # 0 right
    # 1 down
    # 2 left
    # 3 up

    moves = []
    if password == "10R5L5R10L4R5L5\n": moves = [(10, 'R'), (5, "L"),
                 (5, "R"),
                 (10, "L"),
                 (4, "R"),
                 (5, "L"),
                 (5, "N")
                ]
    else:
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


    # Cube l
    #
    #
    # Connectivity
    #
    # 6 faces, 4 transitions, warps position and direction
    #
    #      21
    #      3
    #     54
    #     6
    #
    #     Folding around 4, 2 is the top. 
    #
    #     1:    2 normal, 6, 4, 3 warp, opposite 5
    #     2: 1, 3 normal, 5, 6    warp, opposite 4
    #     3: 2, 4 normal, 1, 5    warp, opposite 6
    #     4: 3, 5 normal, 1, 6    warp, opposite 2
    #     5: 4, 6 normal, 3, 2    warp, opposite 1
    #     6:    5 normal, 4, 2, 1 warp, opposite 3
    #
    # Identifying vertices and edges


    def wrap_example(position, direction):

        # TODO: face data with left, top, right, bottom and orientation of edges
        # TODO: encode the region instead of checking global position
        # TODO: assert the transition is correct

        #     0  1x  3x 
        #     +1   2x  4x
        # 0
        # +1       A-B
        #          |1|
        # 1x   B-A-X-C
        #      |2|3|4|
        # 2x   D-E-Y-Z-C
        #          |5|6|
        # 3x       E-D-B

        size = 4
        row, col = position[0], position[1]
        pos, ang = None, None
        # Edges up and down
        #
        # There are 14 warping edges, 8 up/down, 6 left/right
        if row == 0:
            # 1^ABv2
            ang = 1
            pos = [size+1, size - (col  - 2*size)]
        elif row == size:
            if 1 <= col <= size:
                # 2^BAv1
                ang = 1
                pos = [1, 3*size + 1 - col]
            elif size+1 <= col <= 2*size:
                # 3^AX>1
                ang = 0
                pos = [col - size, 2 * size + 1]
        elif row == 2*size:
            # 6^ZC<4
            ang = 2
            pos = [2*size+1 - (col  - 3*size), 3 * size]
        elif row == 2*size + 1:
            if 1 <= col <= size:
                # 2vDE^5
                ang = 3
                pos = [3*size, 3*size + 1 - col]
            elif size+1 <= col <= 2*size:
                # 3vEY>5
                ang = 0
                pos = [3*size + 1 - (col - size), 2*size + 1]
        elif row == 3*size + 1:
            if 2*size+1 <= col <= 3*size:
                # 5vED^2
                ang = 3
                pos = [2*size, size + 1 - (col - 2*size)]
            elif 3*size + 1 <= col <= 4*size:
                # 6vDB>2
                ang = 0
                pos = [2*size + 1 - (col - 3*size), 1]

        # Left-right edges
        elif col == 0:
            # 2<BD^6
            ang = 3
            pos = [3*size, 3*size + 1 - (row - size)]
        elif col == 2*size:
            if 1 <= row <= size:
                # 1<AXv3
                ang = 1
                pos = [size + 1, row - size]
            elif 2*size+1 <= row <= 3*size:
                # 5<YE^3
                ang = 3
                pos = [2*size, 2*size + 1 - (row - 2*size)]
        elif col == 3*size+1:
            if 1 <= row <= size:
                # 1>BC<4
                ang = 2
                pos = [3*size + 1 - (row - 0), 4*size]
            elif size+1 <= row <= 2*size:
                # 4>CZv6
                ang = 1
                pos = [2*size + 1, 4*size + 1 - (row - size)]
        elif col == 4*size + 1:
            # 6>CB<1
            ang = 2
            pos = [size+1 - (row - 2*size), 2*size]

        if pos is None or ang is None:
            breakpoint()
            print("Bleh got soemthing wrong with", pos, ang)


        return pos, ang

    def wrap_input(position, direction):
        #     0  1x  3x 
        #     +1   2x  4x
        # 0
        # +1     D-C-B
        #        |2|1|
        # 1x     E-X-A
        #        |3|  
        # 2x   E-Y-A    
        #      |5|4|
        # 3x   D-Z-B
        #      |6|
        #      C-B

        # TODO: use direction to know which part of the face data to use
        #       0: right, 1: down, etc

        size = 50
        row, col = position[0], position[1]
        pos, ang = None, None
        if row == 0:
            # 1< or 2<
            if size+1 <= col <= 2*size:
                # warp: 2^DC>6
                pos = [3*size + (col - size), 1]
                ang = 0
            elif 2*size + 1 <= col <= 3*size:
                # warp: 1^CB^6
                pos = [4*size, col - 2*size]
                ang = 3
        elif row == size + 1:
            # warp: 1vXA<3
            ang = 2
            pos = [col - size, 2*size]
        elif row == 2 * size:
            # warp: 5^EY>3
            ang = 0
            pos = [size + col, size + 1]
        elif row == 3*size + 1:
            # down out of 4 into 6
            # warp: 4vZB<6
            ang = 2
            pos = [3*size + col - size, 50]
        elif row == 4*size + 1:
            # warp: 6vCBv1
            ang = 1
            pos = [1, 2*size + col]

        # Left-right
        elif col == 0:
            # 5 or 6
            if 2*size+1 <= row <= 3*size:
                # warp: 5<ED>2
                ang = 0
                # 101 -> 50
                # 150 -> 1
                pos = [3*size + 1 - row, size+1]
            elif 3*size+1 <= row <= 4*size:
                # warp: 6<DCv2
                ang = 1
                pos = [1, size + row - 3*size]
        elif col == size:
            # 2 or 3
            if 1 <= row <= size:
                # warp: 2<DE>5
                ang = 0
                # 1 -> 150
                # 50 -> 101
                pos = [3*size + 1 - row, 1]
            elif size+1 <= row <= 2*size:
                # 3<-5
                # warp: 3<EYv5
                ang = 1
                pos = [2*size + 1, row - size] 
        elif col == size+1:
            # warp: 6>ZB^4
            ang = 3
            pos = [3*size, size + row - 3*size]
        elif col == 2*size + 1:
            # 3 or 4
            if size+1 <= row <= 2*size:
                # 3->1
                # warp: 3>XA^1
                ang = 3
                pos = [size, 2*size + row - size]
            elif 2*size+1 <= row <= 3*size:
                ang = 2
                # warp: 4>AB<1
                # 101 -> 50
                # 150 -> 1
                pos = [3*size+1 - row, 3*size]
        elif col == 3*size + 1:
            # 1->4
            # warp: 1>BA<4
            ang = 2
            pos = [3*size + 1 - row, 2*size]


        if pos is None or ang is None:
            breakpoint()

        return pos, ang


    # Find first 1 in first row

    if "example" in str(filename):
        position = [1, 9]
        wrap = wrap_example
    else:
        position = [1, 51]
        wrap = wrap_input

    direction = 0

    for mix, move in enumerate(moves):
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

                next_square = board[forwards[0], forwards[1]]
                ang = direction
                # Wrapping around, replace next square
                if next_square == 0:
                    #if mix == 87:
                        #    breakpoint()
                    forwards, ang = wrap(forwards, direction)
                    next_square = board[forwards[0], forwards[1]] 
                    
                if next_square == 1:
                    stepped = True
                    position = forwards
                    direction = ang
                    print("Stepped into", position, direction)
                    pathchar = {0: '>', 1: 'v', 2: '<', 3: '^'}[direction]
                    pathboard[position[0], position[1]] = pathchar

                    if 86 < mix < 100:
                        print("\n".join("".join(line) for line in pathboard))
                        print(mix, move, "/", len(moves))
                        #breakpoint()
                elif next_square == 2:
                    # Don't change position or angle if we'd step into a wall
                    stepped = True

        if turn == "R":
            direction = (direction + 1) % 4
        if turn == "L":
            direction = (direction - 1) % 4

        print("Facing", direction)
                


    print("\n".join("".join(line) for line in pathboard))

    #print(board, password)
    breakpoint()
    print(position, direction)

    part1 = 1000 * position[0] + 4 * position[1] + direction

    print("part1:", part1)
    print("part2:", part2)


#day22(examples("22"))
day22(inputs("22"))
