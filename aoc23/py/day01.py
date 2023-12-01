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

regex = "0|1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine"
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

word_to_digit = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def day01(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        total = 0
        word_total = 0
        calibs = []
        for line in puzzlein:

            results = re.findall(regex, line)
            simple = re.findall(regex_simple, line)

            #if len(results) < 2:
            #    breakpoint()

            number = int(str(values[results[0]]) + str(values[results[-1]]))
            #print(line, number)

            if str(number) != word_to_digit.get(results[0], results[0]) + word_to_digit.get(results[-1], results[-1]):
                breakpoint()

            #simple_number = int(simple[0] + simple[-1])
            #total += simple_number
            word_total += number 
            calibs.append(number)
            print(line, number, results)
            breakpoint()

        print(total)
        print(word_total)
        print(calibs)
        print(sum(calibs))
        print(len(calibs))


    print("part1", total)
    print("part2", word_total)


day01(examples("01"))
day01(inputs("01"))
