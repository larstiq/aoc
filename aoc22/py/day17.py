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


@dataclass
class Block:
    lr: int
    td: int
    shape: int
    stopped: bool

    def left(self):
        if self.lr > 0:
            self.lr -= 1

    def right(self):
        shape = self.shape
        # 0123456
        #   ####
        if shape == 0:
            if self.lr < 3:
                self.lr += 1

        # 0123456
        #    #
        #   ###
        #    #
        #
        # 0123456
        #     #
        #     #
        #   ###
        elif shape in (1, 2):
            if self.lr < 4:
                self.lr += 1


        # 0123456
        #   #
        #   #
        #   #
        #   #
        elif shape == 3:
            if self.lr < 6:
                self.lr += 1

        # 0123456
        #
        #   ##
        #   ##

        elif shape == 3:
            if self.lr < 5:
                self.lr += 1


    def down(self, tops):
        if self.stopped:
            return

        if self.td > max(tops) + 1:
            self.td -= 1
            return


        # Now it depends on the shape
        shape = self.shape
        if shape == 3:
            self.stopped = True

        if shape == 4:
            if self.td - 1 in (tops[self.lr], tops[self.lr + 1]):
                self.stopped = True
            else:
                self.td -= 1

        if shape == 2:
            breakpoint()
            if self.td - 1 in tops[self.lr:self.lr + 3]:
                self.stopped = True
            else:
                self.td -= 1

        if shape == 1:
            if self.td - 1 == tops[self.lr + 1] or (self.td + 1) in (tops[self.lr], tops[self.lr + 2]):
                self.stopped = True
            else:
                self.td -= 1

        if shape == 0:
            if self.td - 1 in tops[self.lr:self.lr + 41]:
                self.stopped = True
            else:
                self.td -= 1

    def update_tops(self, tops):
        shape = self.shape
        if shape == 4:
            tops[self.lr] = self.td + 1
            tops[self.lr + 1] = self.td + 1

        if shape == 3:
            tops[self.lr] = self.td + 3

        if shape == 2:
            tops[self.lr] = self.td
            tops[self.lr + 1] = self.td
            tops[self.lr + 2] = self.td + 2

        if shape == 1:
            tops[self.lr] = self.td + 1
            tops[self.lr + 1] = self.td + 2
            tops[self.lr + 2] = self.td + 1

        if shape == 0:
            tops[self.lr] = self.td
            tops[self.lr + 1] = self.td
            tops[self.lr + 2] = self.td
            tops[self.lr + 3] = self.td



def blocks(lr, td):
    pass

def day17(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        jetpattern = puzzlein.read().strip()

    jet = -1
    tops = [0, 0, 0, 0, 0, 0, 0]
    assert len(tops) == 7

    breakpoint()
    for iblock in range(0, 10):
        block = Block(lr=2, td=max(tops) + 4, shape=iblock % 5, stopped=False)
        while not block.stopped:
            jet += 1
            jet %= len(jetpattern)

            print("Jet", jet, "pattern", jetpattern[jet], end=' ,')
            if jetpattern[jet] == '<':
                block.left()
            else:
                block.right()

            # down
            block.down(tops)
            print(block, tops)
        
        block.update_tops(tops)
        print(iblock, tops)
        print()







logging.getLogger().setLevel(logging.WARN)

day17(examples("17"))
#day17(inputs("17"))
