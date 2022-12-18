#!/usr/bin/env python

import itertools
import logging
import math
from dataclasses import dataclass

import more_itertools

from utils import examples, inputs


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
            if (
                field[td + 0][self.lr + 0] == True or
                field[td + 1][self.lr - 1] == True or
                field[td + 2][self.lr + 0] == True
            ):
                return
        elif shape == 2:
            if (
                field[td + 0][self.lr - 1] == True or
                field[td + 1][self.lr + 1] == True or
                field[td + 2][self.lr + 1] == True
            ):
                return
        elif shape == 3:
            if (
                field[td + 0][self.lr - 1] == True or
                field[td + 1][self.lr - 1] == True or
                field[td + 2][self.lr - 1] == True or
                field[td + 3][self.lr - 1] == True
            ):
                return
        elif shape == 4:
            if (
                field[td + 0][self.lr - 1] == True or
                field[td + 1][self.lr - 1] == True
            ):
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
            if (
                field[td + 0][self.lr + 2] == False and
                field[td + 1][self.lr + 3] == False and
                field[td + 2][self.lr + 2] == False
            ):
                self.lr += 1

        # 0123456
        #       #
        #       #
        #     ###
        elif shape == 2:
            if (
                field[td + 0][self.lr + 3] == False and
                field[td + 1][self.lr + 3] == False and
                field[td + 2][self.lr + 3] == False
            ):
                self.lr += 1
        # 0123456
        #       #
        #       #
        #       #
        #       #
        elif shape == 3:
            if (
                field[td + 0][self.lr + 1] == False and
                field[td + 1][self.lr + 1] == False and
                field[td + 2][self.lr + 1] == False and
                field[td + 3][self.lr + 1] == False
            ):
                self.lr += 1

        # 0123456
        #
        #      ##
        #      ##
        elif shape == 4:
            if (
                field[td + 0][self.lr + 2] == False and
                field[td + 1][self.lr + 2] == False
            ):
                self.lr += 1

    def down(self, field):
        if self.stopped:
            return

        if self.td == 1:
            self.stopped = True
            return

        td = self.td
        shape = self.shape
        if shape == 3:
            if field[td - 1][self.lr] == True:
                self.stopped = True
                return

        elif shape == 4:
            if (
                field[td - 1][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True
            ):
                self.stopped = True
                return

        elif shape == 2:
            if (
                field[td - 1][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True or
                field[td - 1][self.lr + 2] == True
            ):
                self.stopped = True
                return

        #      #
        #     ###
        #  td  #
        #     012
        elif shape == 1:
            if (
                field[td + 0][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True or
                field[td + 0][self.lr + 2] == True
            ):
                self.stopped = True
                return

        elif shape == 0:
            if (
                field[td - 1][self.lr + 0] == True or
                field[td - 1][self.lr + 1] == True or
                field[td - 1][self.lr + 2] == True or
                field[td - 1][self.lr + 3] == True
            ):
                self.stopped = True
                return

        self.td -= 1

    def update_tops(self, field):
        shape = self.shape
        td = self.td
        if shape == 4:
            field[td + 0][self.lr : self.lr + 2] = True, True
            field[td + 1][self.lr : self.lr + 2] = True, True

        if shape == 3:
            field[td + 0][self.lr] = True
            field[td + 1][self.lr] = True
            field[td + 2][self.lr] = True
            field[td + 3][self.lr] = True

        if shape == 2:
            field[td + 0][self.lr : self.lr + 3] = True, True, True
            field[td + 1][self.lr + 2] = True
            field[td + 2][self.lr + 2] = True

        if shape == 1:
            field[td + 0][self.lr + 1] = True
            field[td + 1][self.lr : self.lr + 3] = True, True, True
            field[td + 2][self.lr + 1] = True

        if shape == 0:
            field[td][self.lr : self.lr + 4] = True, True, True, True


def display_field(field, start, top):

    dis_start = min(len(field) - 1, top - start)
    for row in range(dis_start, 0, -1):
        print(f"{start + row:<5}", "".join("#" if cell else "." for cell in field[row]))


def day17(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        gusts = puzzlein.read().strip()
        data = [-1 if j == "<" else 1 for j in gusts]
        jetpattern = itertools.cycle(data)

    top = 0

    widths = [4, 3, 3, 1, 2]
    tops = [0, 2, 2, 3, 1]

    max_cycle_length = len(data) * 5
    field_size = 4 * max(2022, max_cycle_length)
    field = [
        [False, False, False, False, False, False, False] for _ in range(field_size)
    ]
    # Absolute zero
    field[0] = [True, True, True, True, True, True, True]

    track_tops = []
    for iblock in range(0, max(2022, max_cycle_length)):
        pos = 2

        shape = iblock % 5
        width = widths[shape]

        moves = more_itertools.take(4, jetpattern)
        for move in moves:
            pos = min(7 - width, max(0, pos + move))

        block = Block(lr=pos, td=top + 1, shape=shape, stopped=False)
        block.down(field)

        while not block.stopped:
            move = next(jetpattern)

            if move == -1:
                block.left(field)
            else:
                block.right(field)

            block.down(field)

        block.update_tops(field)
        top = max(top, block.td + tops[shape])
        track_tops.append(top)

    print("part1:", track_tops[2022 - 1])

    differences = [r - l for (l, r) in more_itertools.pairwise(track_tops[500:])]
    for seq_len in range(2, math.ceil(len(differences) / 2)):
        if differences[0:seq_len] == differences[seq_len : 2 * seq_len]:
            break

    # It will take days to run the simulation as far as the elepehants want,
    # but the blocks repeat (there are 5 blocks we cycle through and the gusts cycle too)
    equiv_class = (1000000000000 - 1) % seq_len
    equiv_value = track_tops[equiv_class]
    blocks_per_cycle = track_tops[equiv_class + seq_len] - equiv_value
    total_blocks = (
        equiv_value + blocks_per_cycle * ((1000000000000 - 1) - equiv_class) // seq_len
    )
    print("sequence cycle length:", seq_len)
    print("part2:", total_blocks)


logging.getLogger().setLevel(logging.WARN)

day17(examples("17"))
day17(inputs("17"))
