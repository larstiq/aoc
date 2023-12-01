#!/usr/bin/env python

from utils import inputs, examples

import regex as re

digits = list("0123456789")
words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

word_to_digit = { word: str(ix) for (ix, word) in enumerate(words) }
values = {str(d): d for d in range(10)} | {word: ix for (ix, word) in enumerate(words) }
digits_regex = "|".join(digits)
words_regex = "|".join(digits + words)


def calibration_number(symbols, line):
    try:
        results = re.findall(symbols, line, overlapped=True)
        number = int(str(values[results[0]]) + str(values[results[-1]]))
    except:
        number = 0
    return number

def day01(filename):
    print()
    print(filename)

    with open(filename) as puzzlein:
        calibration_digits = []
        calibration_words = []
        for line in puzzlein:
            line = line.strip()

            calibration_digits.append(calibration_number(digits_regex, line))
            calibration_words.append(calibration_number(words_regex, line))

    print("part1", sum(calibration_digits))
    print("part2", sum(calibration_words))

day01(examples("01"))
day01(inputs("01"))
