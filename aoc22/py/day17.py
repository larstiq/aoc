#!/usr/bin/env python

from utils import inputs, examples

import functools
import json
import logging
import math

import more_itertools
import networkx as nx

from collections import defaultdict
from dataclasses import dataclass

import numpy as np


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
        if shape == 0:
            # Is the cell left to us free?
            if field[self.td, self.lr - 1] == False:
                self.lr -= 1
        elif shape == 1:
            # Are the cells left of the edge free?
            if (field[self.td, self.lr] == False and
                field[self.td + 1, self.lr - 1] == False and
                field[self.td + 2, self.lr] == False):
                self.lr -= 1
        elif shape == 2:
            #breakpoint()
            if (field[self.td, self.lr - 1] == False and
                field[self.td + 1, self.lr + 1] == False and
                field[self.td + 2, self.lr + 1] == False):
                self.lr -= 1
        elif shape == 3:
            if (field[self.td, self.lr - 1] == False and
                field[self.td + 1, self.lr - 1] == False and
                field[self.td + 2, self.lr - 1] == False and
                field[self.td + 3, self.lr - 1] == False):
                self.lr -= 1
        elif shape == 4:
            if (field[self.td, self.lr - 1] == False and
                field[self.td + 1, self.lr - 1] == False):
                self.lr -= 1


    def right(self, field):
        shape = self.shape

        # 0123456
        #    ####
        if shape == 0:
            if self.lr == 3:
                return
            # Is the cell left to us free?
            if field[self.td, self.lr + 4] == False:
                self.lr += 1

        # 0123456
        #      #
        #     ###
        #      #
        elif shape == 1:
            if self.lr == 4:
                return
            # Are the cells right of the edge free?
            if (field[self.td, self.lr + 2] == False and
                field[self.td + 1, self.lr + 3] == False and
                field[self.td + 2, self.lr + 2] == False):
                self.lr += 1

        # 0123456
        #       #
        #       #
        #     ###
        elif shape == 2:
            if self.lr == 4:
                return
            if (field[self.td, self.lr + 3] == False and
                field[self.td + 1, self.lr + 3] == False and
                field[self.td + 2, self.lr + 3] == False):
                self.lr += 1
        # 0123456
        #       #
        #       #
        #       #
        #       #
        elif shape == 3:
            if self.lr == 6:
                return
            if (field[self.td, self.lr + 1] == False and
                field[self.td + 1, self.lr + 1] == False and
                field[self.td + 2, self.lr + 1] == False and
                field[self.td + 3, self.lr + 1] == False):
                self.lr += 1

        # 0123456
        #
        #      ##
        #      ##
        elif shape == 4:
            if self.lr == 5:
                return
            if (field[self.td, self.lr + 2] == False and
                field[self.td + 1, self.lr + 2] == False):
                self.lr += 1


    def down(self, field):
        if self.stopped:
            return

        if self.td == 1:
            self.stopped = True
            return

        shape = self.shape
        if shape == 3:
            if field[self.td - 1, self.lr] == True:
                self.stopped = True
            else:
                self.td -= 1

        elif shape == 4:
            if (field[self.td - 1, self.lr] == False and
                field[self.td - 1, self.lr + 1] == False):
                self.td -= 1
            else:
                self.stopped = True

        elif shape == 2:
            if (field[self.td - 1, self.lr] == False and
                field[self.td - 1, self.lr + 1] == False and
                field[self.td - 1, self.lr + 2] == False):
                self.td -= 1
            else:
                self.stopped = True

        elif shape == 1:
            if (field[self.td , self.lr] == False and
                field[self.td - 1, self.lr + 1] == False and
                field[self.td, self.lr + 2] == False):
                self.td -= 1
            else:
                self.stopped = True

        elif shape == 0:
            if (field[self.td - 1, self.lr] == False and
                field[self.td - 1, self.lr + 1] == False and
                field[self.td - 1, self.lr + 2] == False and
                field[self.td - 1, self.lr + 3] == False):
                self.td -= 1
            else:
                self.stopped = True

    def update_tops(self, field):
        shape = self.shape
        if shape == 4:
            field[self.td:self.td + 2, self.lr:self.lr + 2] = True

        if shape == 3:
            field[self.td:self.td + 4, self.lr] = True

        if shape == 2:
            field[self.td, self.lr:self.lr + 3] = True
            field[self.td + 1, self.lr + 2] = True
            field[self.td + 2, self.lr + 2] = True

        if shape == 1:
            field[self.td, self.lr + 1] = True
            field[self.td + 1, self.lr:self.lr + 3] = True
            field[self.td + 2, self.lr + 1] = True

        if shape == 0:
            field[self.td, self.lr:self.lr + 4] = True

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



def display_field(field):
    for row in range(field.shape[0] - 1, 0, -1):
        print("".join("#" if cell else "." for cell in field[row, :]))

def day17(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        jetpattern = puzzlein.read().strip()

    jet = -1


    top = 0
    field = np.zeros((5000, 7), dtype=bool)
    for iblock in range(0, 2022):
        block = Block(lr=2, td=top + 4, shape=iblock % 5, stopped=False)
        while not block.stopped:
            jet += 1
            jet %= len(jetpattern)

            if jetpattern[jet] == '<':
                block.left(field)
            else:
                block.right(field)

            # down
            block.down(field)
            logging.debug("Jet %s pattern %s : %s, %s", jet, jetpattern[jet], block, top) 
        
        block.update_tops(field)
        top = max(top, block.top())
        
        if iblock % 100 == 0:
            display_field(field[:top + 1, :])
            print(iblock, top)
            print()

    for row in range(field.shape[0] - 1, 0, -1):
        if field[row, :].any():
            print("part1:", row)
            break

    breakpoint()






logging.getLogger().setLevel(logging.WARN)

day17(examples("17"))
day17(inputs("17"))
