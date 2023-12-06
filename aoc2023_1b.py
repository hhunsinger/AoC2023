# https://adventofcode.com/2023/day/1

import re

# test data
# solution = 281
calibrations = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen'
]

# real data
f = open("private/aoc2023_1_input.txt", "r")
calibrations = f.readlines()
f.close()

numbers_spelled = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
    ]
numbers = []
num_dict = {
    'one' : 1,
    'two' : 2,
    'three' : 3,
    'four' : 4,
    'five' : 5,
    'six' : 6,
    'seven' : 7,
    'eight' : 8,
    'nine' : 9
}
for line in calibrations:
    line_numbers = []
    matches = re.findall(r"(?=(\d|"+'|'.join(numbers_spelled)+r"))", line)
    for i in matches:
        if i.isnumeric():
            line_numbers.append(i)
        elif num_dict.get(i,None):
            line_numbers.append(num_dict[i])
    length = len(line_numbers)
    if length > 0:
        firstnum = line_numbers[0]
        lastnum = line_numbers[length-1]
        fullnum_str = "%s%s" % (firstnum, lastnum)
        fullnum = int(fullnum_str)
        numbers.append(fullnum)
total = sum(numbers)

print("part 2 answer:", total)
