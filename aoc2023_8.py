
# https://adventofcode.com/2023/day/8

import re

# test data
# solution part 1 = 2
nodes_raw = [
    'RL',
    '',
    'AAA = (BBB, CCC)',
    'BBB = (DDD, EEE)',
    'CCC = (ZZZ, GGG)',
    'DDD = (DDD, DDD)',
    'EEE = (EEE, EEE)',
    'GGG = (GGG, GGG)',
    'ZZZ = (ZZZ, ZZZ)'
]

# test data
# solution part 1 = 6
nodes_raw = [
    'LLR',
    '',
    'AAA = (BBB, BBB)',
    'BBB = (AAA, ZZZ)',
    'ZZZ = (ZZZ, ZZZ)'
]

# actual data
f = open("private/aoc2023_8_input.txt", "r")
nodes_raw = f.readlines()
f.close()

directions = ''
nodes = {}
for line in nodes_raw:
    line = line.strip() # get rid of newline
    if line == '': # skip blank lines
        continue
    elif not '=' in line: # this is the LR direction line
        directions = line
    else: # this is a node line
        match = re.search("^(\w{3}) = \((\w{3}), (\w{3})\)$", line)
        nodes[match.group(1)] = {'L': match.group(2), 'R': match.group(3)}

print(nodes)

# part 1
start_node = 'AAA'
end_node = 'ZZZ'

move_count = 0
next_node = start_node
while next_node != end_node:
    for direction in directions:
        move_count = move_count+1
        next_node = nodes[next_node][direction]

print('answer part 1:', move_count)

# Part 1
# I initially solved with recursion, which worked with the test data but went too many recursion levels deep with the real data.
# Got stuck trying to write an algorithm for traversing the binary tree without recursion. I got a hint that I only need recursion
# if I don't have directions -- but the puzzle gives us directions. So instead I can just iterate thru the directions. Iterating
# through the directions was actually my initial thought when I first started, but I couldn't figure out how to make it loop and
# then stop when necessary. I had forgotten about while loops... XD