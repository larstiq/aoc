#!/usr/bin/env python

from utils import inputs, examples

from collections import defaultdict

from pathlib import Path


def day07(filename):
    print()
    print(filename)

    sizes = {}
    with open(filename) as puzzlein:

        part1 = 0
        part2 = 0
        data = puzzlein.read()
        cwd = Path("/")
        for cmd_output in data.split("$ "):
            if cmd_output.startswith("cd"):
                path = cmd_output[3:].strip()
                if path == "/":
                    cwd = Path("/")
                elif path == "..":
                    cwd = cwd.parent
                else:
                    path = (cwd / path).absolute()
                    cwd = path
            elif cmd_output.startswith("ls\n"):
                for line in cmd_output[3:].strip().split("\n"):
                    size, entry = line.split()
                    if size != "dir":
                        sizes[cwd / entry] = int(size)
            elif cmd_output == "":
                pass

        dir_sizes = defaultdict(int)
        for file_entry, file_size in sizes.items():
            p = file_entry.parent.absolute()
            dir_sizes[p] += file_size
            while p != Path("/"):
                p = p.parent.absolute()
                dir_sizes[p] += file_size

        print(dir_sizes)
        part1 = sum(v for (k, v) in dir_sizes.items() if v <= 100000)
        print("part1:", part1)


day07(inputs("07"))
day07(examples("07"))
