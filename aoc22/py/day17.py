#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools

from collections import defaultdict
from dataclasses import dataclass

import time


@dataclass
class Block:
    lr: int
    td: int
    shape: int
    stopped: bool

    def left(self, field):
        # This works fine for the wall but not for blocks, bleh
        if self.lr == 0:
            return

        shape = self.shape


        td = self.td
        if shape == 0:
            # Is the cell left to us free?
            if field[td][self.lr - 1] == True:
                return
        elif shape == 1:
            # Are the cells left of the edge free?
            if (field[td + 0][self.lr + 0] == True or
                field[td + 1][self.lr - 1] == True or
                field[td + 2][self.lr + 0] == True):
                return
        elif shape == 2:
            #breakpoint()
            if (field[td + 0][self.lr - 1] == True or
                field[td + 1][self.lr + 1] == True or
                field[td + 2][self.lr + 1] == True):
                return
        elif shape == 3:
            if (field[td + 0][self.lr - 1] == True or
                field[td + 1][self.lr - 1] == True or
                field[td + 2][self.lr - 1] == True or
                field[td + 3][self.lr - 1] == True):
                return
        elif shape == 4:
            if (field[td + 0][self.lr - 1] == True or
                field[td + 1][self.lr - 1] == True):
                return

        self.lr -= 1


    def right(self, field):
        shape = self.shape
        td = self.td
        width = [4, 3, 3, 1, 2][shape]

        if 7 - width == self.lr:
            return

        # 0123456
        #    ####
        if shape == 0:
            # Is the cell left to us free?
            if field[td][self.lr + 4] == False:
                self.lr += 1

        # 0123456
        #      #
        #     ###
        #      #
        elif shape == 1:
            # Are the cells right of the edge free?
            if (field[td + 0][self.lr + 2] == False and
                field[td + 1][self.lr + 3] == False and
                field[td + 2][self.lr + 2] == False):
                self.lr += 1

        # 0123456
        #       #
        #       #
        #     ###
        elif shape == 2:
            if (field[td + 0][self.lr + 3] == False and
                field[td + 1][self.lr + 3] == False and
                field[td + 2][self.lr + 3] == False):
                self.lr += 1
        # 0123456
        #       #
        #       #
        #       #
        #       #
        elif shape == 3:
            if (field[td + 0][self.lr + 1] == False and
                field[td + 1][self.lr + 1] == False and
                field[td + 2][self.lr + 1] == False and
                field[td + 3][self.lr + 1] == False):
                self.lr += 1

        # 0123456
        #
        #      ##
        #      ##
        elif shape == 4:
            if (field[td + 0][self.lr + 2] == False and
                field[td + 1][self.lr + 2] == False):
                self.lr += 1


    def down(self, field):
        if self.stopped:
            return

        if self.td == 1:
            self.stopped = True
            return

        td = self.td
        if td < 0:
            breakpoint()

        shape = self.shape
        if shape == 3:
            if field[td - 1][self.lr] == True:
                self.stopped = True
                return

        elif shape == 4:
            if (field[td - 1][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True):
                self.stopped = True
                return

        elif shape == 2:
            if (field[td - 1][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True or
                field[td - 1][self.lr + 2] == True):
                self.stopped = True
                return

        #      #
        #     ###
        #  td  #
        #     012 
        elif shape == 1:
            if (field[td + 0][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True or
                field[td + 0][self.lr + 2] == True):
                self.stopped = True
                return

        elif shape == 0:
            if (field[td - 1][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True or
                field[td - 1][self.lr + 2] == True or
                field[td - 1][self.lr + 3] == True):
                self.stopped = True
                return

        self.td -= 1

    def update_tops(self, field):
        shape = self.shape
        td = self.td
        if shape == 4:
            field[td + 0][self.lr:self.lr + 2] = True, True
            field[td + 1][self.lr:self.lr + 2] = True, True

        if shape == 3:
            field[td + 0][self.lr] = True
            field[td + 1][self.lr] = True
            field[td + 2][self.lr] = True
            field[td + 3][self.lr] = True

        if shape == 2:
            field[td + 0][self.lr:self.lr + 3] = True, True, True
            field[td + 1][self.lr + 2] = True
            field[td + 2][self.lr + 2] = True

        if shape == 1:
            field[td + 0][self.lr + 1] = True
            field[td + 1][self.lr:self.lr + 3] = True, True, True
            field[td + 2][self.lr + 1] = True

        if shape == 0:
            field[td][self.lr:self.lr + 4] = True, True, True, True

    def top(self):
        shape = self.shape
        if shape == 4:
            return self.td + 1

        if shape == 3:
            return self.td + 3

        if shape == 2:
            return self.td + 2

        if shape == 1:
            return self.td + 2

        if shape == 0:
            return self.td



def display_field(field, start, top):

    dis_start = min(len(field) - 1, top - start)
    for row in range(dis_start, 0, -1):
        print(f"{start + row:<5}", "".join("#" if cell else "." for cell in field[row]))



import itertools

def day17(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        gusts = puzzlein.read().strip()
        data = [-1 if j == '<' else 1 for j in gusts]
        jetpattern = itertools.cycle(data)

    top = 0
    field_diff = 2**6
    field_size = 4 * field_diff
    field = [[False, False, False, False, False, False, False] for _ in range(field_size)]
    # Absolute zero
    field[0] = [True, True, True, True, True, True, True]
    start_of_field = 0
    start_computation = time.time()

    widths = [4, 3, 3, 1, 2]
    #for iblock in range(0, 1000000000000):
    for iblock in range(0, 2022):
    #for iblock in range(0, 200000):
        pos = 2

        #if iblock == 13:
            #breakpoint()
            #    pass

        shape = iblock % 5
        width = widths[shape]

        moves = more_itertools.take(4, jetpattern)
        #print("moves for iblock", moves, iblock)
        for move in moves:
            pos = min(7 - width, max(0, pos + move))

        block = Block(lr=pos, td=top + 1, shape=shape, stopped=False)
        block.down(field)

        while not block.stopped:
            move = next(jetpattern)


            #print("another move", move, "for iblock", iblock, "at", block.td)
            #breakpoint()
            #if block.td < 0:
                #breakpoint()

            # Idea 1: we don't need to do the left and right shifting at least
            # until we're at risk of collision, and then we can just sum them
            # up for a total left/right shift
            #
            # When is that?  At the very least we can roll up the first 4 steps that it appears above the rest
            # 
            # Unfortunately we need to deal with the clamping behaviour, can't just pay attention to the sign.
            # 
            # And we do need to know the width of the block to know when to clamp, and that a reversal then goes back.
            #
            # Position +- 1
            # pos = newpos + move

            # if pos + move is negative, return 0
            # if pos + move > 7 - width it means the new position would stick the right end outside, not good either

            if move == -1:
                block.left(field)
            else:
                block.right(field)

            # down
            block.down(field)
            #logging.debug("Jet %s pattern %s : %s, %s", jet, move, block, top) 
        
        block.update_tops(field)
        top = max(top, block.top())

        if iblock % 500000 == 1:
            sofar = int(time.time() - start_computation)
            #display_field(field[:top + 1, :])

            print(iblock / 1000000000000, sofar, iblock, top, sofar * 1000000000000 / iblock / (3600 * 24))
            #print()

        if top > 2 * field_diff:
            #breakpoint()
            # Can we do this without allocating, but a circular buffer?
            new_field = [[False, False, False, False, False, False, False] for _ in range(field_size)]
            new_field[:field_size - field_diff] = field[field_diff:]
            #display_field(field, start_of_field, top)
            field = new_field
            #breakpoint()
            start_of_field += field_diff
            top -= field_diff
            #print('*' * 80)
            #display_field(field, start_of_field, top)

        #display_field(field, start_of_field, top)
        #breakpoint()
        if iblock == 2021:

            for row in range(len(field) - 1, 0, -1):
                if any(field[row]):
                    print("part1:", start_of_field + top)
                    break

    breakpoint()






logging.getLogger().setLevel(logging.WARN)

day17(examples("17"))
day17(inputs("17"))
