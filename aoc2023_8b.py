
# https://adventofcode.com/2023/day/8

import re
from math import lcm

# test data part 2
# solution part 2 = 6
nodes_raw = [
    'LR',
    '',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)'
]

# actual data
f = open("private/aoc2023_8_input.txt", "r")
nodes_raw = f.readlines()
f.close()

directions = ''
nodes = {}
start_nodes = []
end_nodes = []
for line in nodes_raw:
    line = line.strip() # get rid of newline
    if line == '': # skip blank lines
        continue
    elif not '=' in line: # this is the LR direction line
        directions = line
    else: # this is a node line
        match = re.search("^(\w{3}) = \((\w{3}), (\w{3})\)$", line)
        node = match.group(1)
        if node.endswith('A'):
            start_nodes.append(node)
        elif node.endswith('Z'):
            end_nodes.append(node)
        nodes[node] = {
            'L': match.group(2), 
            'R': match.group(3),
        }

# important: networks are circular. end nodes point back to start nodes!

moves = []
for node in start_nodes:
    start_node = node
    move_count = 0
    next_node = start_node
    while next_node not in end_nodes:
        for direction in directions:
            move_count = move_count+1
            next_node = nodes[next_node][direction]
            if next_node in end_nodes: # if we're at the end, don't continue going through `directions`
                break
    moves.append(move_count)

# use lowest common multiple to determine the number of moves that gets all the ghosts to a Z point
print("part 2 answer:", lcm(*moves))

# Part 2
# I got confused for a while because I didn't realize the networks were circular. I thought they could continue going past the Z nodes.
# Once I realized that, I needed a hint on how to know when to stop, so I checked the subreddit and saw a lot of references to LCM.
# Googled it and found "lowest common multiple" which makes sense. Since each network is going in a circle, I just need to know how many
# times around the circle they all have to go to all get to the end at the same time.