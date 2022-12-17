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
import time


@dataclass
class Block:
    lr: int
    td: int
    shape: int
    stopped: bool

    def left(self, start_of_field, field):
        # This works fine for the wall but not for blocks, bleh
        if self.lr == 0:
            return

        shape = self.shape


        td = self.td - start_of_field
        if shape == 0:
            # Is the cell left to us free?
            if field[td, self.lr - 1] == False:
                self.lr -= 1
        elif shape == 1:
            # Are the cells left of the edge free?
            if (field[td, self.lr] == False and
                field[td + 1, self.lr - 1] == False and
                field[td + 2, self.lr] == False):
                self.lr -= 1
        elif shape == 2:
            #breakpoint()
            if (field[td, self.lr - 1] == False and
                field[td + 1, self.lr + 1] == False and
                field[td + 2, self.lr + 1] == False):
                self.lr -= 1
        elif shape == 3:
            if (field[td, self.lr - 1] == False and
                field[td + 1, self.lr - 1] == False and
                field[td + 2, self.lr - 1] == False and
                field[td + 3, self.lr - 1] == False):
                self.lr -= 1
        elif shape == 4:
            if (field[td, self.lr - 1] == False and
                field[td + 1, self.lr - 1] == False):
                self.lr -= 1


    def right(self, start_of_field, field):
        shape = self.shape
        td = self.td - start_of_field

        # 0123456
        #    ####
        if shape == 0:
            if self.lr == 3:
                return
            # Is the cell left to us free?
            if field[td, self.lr + 4] == False:
                self.lr += 1

        # 0123456
        #      #
        #     ###
        #      #
        elif shape == 1:
            if self.lr == 4:
                return
            # Are the cells right of the edge free?
            if (field[td, self.lr + 2] == False and
                field[td + 1, self.lr + 3] == False and
                field[td + 2, self.lr + 2] == False):
                self.lr += 1

        # 0123456
        #       #
        #       #
        #     ###
        elif shape == 2:
            if self.lr == 4:
                return
            if (field[td, self.lr + 3] == False and
                field[td + 1, self.lr + 3] == False and
                field[td + 2, self.lr + 3] == False):
                self.lr += 1
        # 0123456
        #       #
        #       #
        #       #
        #       #
        elif shape == 3:
            if self.lr == 6:
                return
            if (field[td, self.lr + 1] == False and
                field[td + 1, self.lr + 1] == False and
                field[td + 2, self.lr + 1] == False and
                field[td + 3, self.lr + 1] == False):
                self.lr += 1

        # 0123456
        #
        #      ##
        #      ##
        elif shape == 4:
            if self.lr == 5:
                return
            if (field[td, self.lr + 2] == False and
                field[td + 1, self.lr + 2] == False):
                self.lr += 1


    def down(self, start_of_field, field):
        if self.stopped:
            return

        if self.td == 1:
            self.stopped = True
            return

        td = self.td - start_of_field

        shape = self.shape
        if shape == 3:
            if field[td - 1, self.lr] == True:
                self.stopped = True
            else:
                self.td -= 1

        elif shape == 4:
            if (field[td - 1, self.lr] == False and
                field[td - 1, self.lr + 1] == False):
                self.td -= 1
            else:
                self.stopped = True

        elif shape == 2:
            if (field[td - 1, self.lr] == False and
                field[td - 1, self.lr + 1] == False and
                field[td - 1, self.lr + 2] == False):
                self.td -= 1
            else:
                self.stopped = True

        elif shape == 1:
            if (field[td , self.lr] == False and
                field[td - 1, self.lr + 1] == False and
                field[td, self.lr + 2] == False):
                self.td -= 1
            else:
                self.stopped = True

        elif shape == 0:
            if (field[td - 1, self.lr] == False and
                field[td - 1, self.lr + 1] == False and
                field[td - 1, self.lr + 2] == False and
                field[td - 1, self.lr + 3] == False):
                self.td -= 1
            else:
                self.stopped = True

    def update_tops(self, start_of_field, field):
        shape = self.shape
        td = self.td - start_of_field
        if shape == 4:
            field[td:td + 2, self.lr:self.lr + 2] = True

        if shape == 3:
            field[td:td + 4, self.lr] = True

        if shape == 2:
            field[td, self.lr:self.lr + 3] = True
            field[td + 1, self.lr + 2] = True
            field[td + 2, self.lr + 2] = True

        if shape == 1:
            field[td, self.lr + 1] = True
            field[td + 1, self.lr:self.lr + 3] = True
            field[td + 2, self.lr + 1] = True

        if shape == 0:
            field[td, self.lr:self.lr + 4] = True

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

    dis_start = min(field.shape[0] - 1, top - start)
    for row in range(dis_start, 0, -1):
        print(f"{start + row:<5}", "".join("#" if cell else "." for cell in field[row, :]))

def day17(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        jetpattern = puzzlein.read().strip()

    jet = -1


    top = 0
    field_size = 50000
    field = np.zeros((field_size, 7), dtype=bool)
    start_of_field = 0
    start_computation = time.time()
    for iblock in range(0, 1000000000000):
        #for iblock in range(0, 2022):
        block = Block(lr=2, td=top + 4, shape=iblock % 5, stopped=False)
        while not block.stopped:
            jet += 1
            jet %= len(jetpattern)

            # Idea 1: we don't need to do the left and right shifting at least
            # until we're at risk of collision, and then we can just sum them
            # up for a total left/right shift
            #
            # When is that? 
            if jetpattern[jet] == '<':
                block.left(start_of_field, field)
            else:
                block.right(start_of_field, field)

            # down
            block.down(start_of_field, field)
            logging.debug("Jet %s pattern %s : %s, %s", jet, jetpattern[jet], block, top) 
        
        block.update_tops(start_of_field, field)
        top = max(top, block.top())

        if iblock % 50000 == 0:
            #display_field(field[:top + 1, :])
            print(iblock / 1000000000000, int(time.time() - start_computation), iblock, top)
            #print()

        field_diff = 10000
        if top - start_of_field > 2 * field_diff:
            #breakpoint()
            new_field = np.zeros((field_size, 7), dtype=bool)
            new_field[:field_size - field_diff, :] = field[field_diff:, :]
            #display_field(field, start_of_field, top)
            field = new_field
            start_of_field += field_diff
            #print('*' * 80)
            #display_field(field, start_of_field, top)

    for row in range(field.shape[0] - 1, 0, -1):
        if field[row, :].any():
            print("part1:", top)
            break

    #breakpoint()






logging.getLogger().setLevel(logging.WARN)

day17(examples("17"))
day17(inputs("17"))
