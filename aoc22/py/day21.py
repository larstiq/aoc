#!/usr/bin/env python

from utils import examples, inputs

from collections import defaultdict, deque
import time

import numpy as np
import re

import networkx as nx
import sympy

from dataclasses import dataclass


def day21(filename):
    print()
    print(filename)

    part1 = 0
    part2 = 0

    tree = nx.DiGraph()
    leaf_monkeys = set()


    siblings = dict()

    with open(filename) as puzzlein:
        for line in puzzlein:
            name, expression = line.split(":")
            expression = expression.strip()
            words = expression.split()
            if len(words) > 1:
                left, right = sympy.symbols(' '.join([words[0], words[2]]))
                if words[1] == '+':
                    expr = left + right
                elif words[1] == '*': 
                    expr = left * right
                elif words[1] == '/': 
                    expr = left / right
                elif words[1] == '-': 
                    expr = left - right
                else:
                    breakpoint()

                tree.add_node(name, expr=expr)


                siblings[words[0]] = words[-1]
                siblings[words[-1]] = words[0]
                for input_monkey in [words[0], words[-1]]:
                    tree.add_edge(input_monkey, name)
            else:
                if name == 'humn':
                    expr = sympy.parse_expr('humn')
                    value = expr
                elif name == 'root':
                    expr = expression
                else:
                    expr = expression
                    value = int(expression)

                tree.add_node(name, expr=expr)
                tree.nodes[name]['value'] = value
                leaf_monkeys.add(name)


    while leaf_monkeys != {'root'}:
        for m in sorted(leaf_monkeys):
            sibling_name = siblings[m]
            sibling = tree.nodes[sibling_name]

            if 'value' not in sibling:
                continue

            parent_name, = tree[m]
            parent = tree.nodes[parent_name]

            if 'value' in parent:
                pass
            else:
                parent['value'] = parent['expr'].subs({m: tree.nodes[m]['value'], sibling_name: sibling['value']})
                leaf_monkeys.remove(m)
                leaf_monkeys.add(parent_name)

            if sibling_name in leaf_monkeys:
                leaf_monkeys.remove(sibling_name)


    print(leaf_monkeys)
    print(siblings)

    breakpoint()
    print("part1:", tree.nodes['root'])
    print("part2:", part2)


day21(examples("21"))
day21(inputs("21"))
