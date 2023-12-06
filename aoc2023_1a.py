# https://adventofcode.com/2023/day/1

# test data
# solution = 142
calibrations = [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet'
]

# real data
f = open("private/aoc2023_1_input.txt", "r")
calibrations = f.readlines()
f.close()

numbers = []
for line in calibrations:
    line_numbers = []
    for i in line:
        if i.isnumeric():
            line_numbers.append(i)
    length = len(line_numbers)
    if length > 0:
        firstnum = line_numbers[0]
        lastnum = line_numbers[length-1]
        fullnum_str = "%s%s" % (firstnum, lastnum)
        fullnum = int(fullnum_str)
        numbers.append(fullnum)
total = sum(numbers)

print("part 1 answer:", total)