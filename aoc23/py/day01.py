#!/usr/bin/env python

from utils import inputs, examples

import re

words = [
"zero",
"one",
"two",
"three",
"four",
"five",
"six",
"seven",
"eight",
"nine",
]

regex = "0|1|2|3|4|5|6|7|8|9|zero|one|two|three|four|five|six|seven|eight|nine"
regex_simple = "0|1|2|3|4|5|6|7|8|9"

values = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def day01(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        total = 0
        word_total = 0
        for line in puzzlein:

            digits = [(ix, char) for (ix, char) in enumerate(line) if char in "0123456789"]


            results = re.findall(regex, line)
            simple = re.findall(regex_simple, line)
            #print(results)
            #print(results[0], results[-1])
            #print(values[results[0]], values[results[-1]])

            number = int(str(values[results[0]]) + str(values[results[-1]]))
            print(line, number)

            #simple_number = int(simple[0] + simple[-1])

            #total += simple_number
            breakpoint()
            word_total += number 

        print(total)
        print(word_total)


    print("part1", total)
    print("part2", word_total)


day01(examples("01"))
day01(inputs("01"))
