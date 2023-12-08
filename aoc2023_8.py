# https://adventofcode.com/2023/day/8

import re

# test data
# solution part 1 = 2
nodes_raw = [
    'RL',
    '',
    'AAA = (BBB, CCC)', # this is a tuple - can i just execute it directly rather than parsing it manually?
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

# print(directions)
# print(nodes)

start_node = 'AAA'
end_node = 'ZZZ'

def get_next_node(node, direction_index, move_count, end_node):
    move_count = move_count+1
    # print('move count', move_count)
    direction = directions[direction_index]
    next_node = nodes[node][direction]
    if next_node == end_node: # we're done
        print('answer part 1:', move_count)
        return move_count
    else: # recurse
        if direction_index+1 >= len(directions):
            next_direction_index = 0
        else:
            next_direction_index = direction_index+1
        get_next_node(next_node, next_direction_index, move_count, end_node)

move_count_final = get_next_node(start_node, 0, 0, end_node)
# print(move_count_final) # TODO why isn't this working? is it not bubbling up?
# NOT DONE - there's a bug, maximum recursion depth reached