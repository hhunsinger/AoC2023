# https://adventofcode.com/2023/day/11

import re

# test data
# solution part 1 = 374
# solution part 2 = 82000210
lines_raw = [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....'
]

# actual data
def load_input(file='private/aoc2023_11_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

lines_raw = load_input()

# how wide is our matrix to start?
column_count_start = len(lines_raw[0])

# expand horizontally
columns_to_expand = []
for i in range(0,column_count_start):
    count = 0
    for line in lines_raw:
        if line[i] == '#':
            count = count+1
    # if we didn't find any galaxies in this column, 
    # add it to the list of columns to expand
    if count == 0:
        columns_to_expand.append(i)
# we want to add starting with the last column, otherwise all 
# columns after the first one are added in the wrong place
columns_to_expand.sort(reverse=True) 
widened_map = []
for line in lines_raw:
    new_line = line
    for column in columns_to_expand:
        new_line = new_line[:column] + '.' + new_line[column:]
    widened_map.append(new_line)

# what's our final matrix width?
column_count = len(widened_map[0])

# find all the galaxies and expand the matrix vertically
galaxies_map = []
for line in widened_map:
    line_galaxies = []
    p = re.compile("#")
    for m in p.finditer(line):
        line_galaxies.append(m.start())
    galaxies_map.append(line_galaxies)
    # expand vertically
    if line_galaxies == []: # if there's no galaxies in this line, expand by 1
        galaxies_map.append([])

def get_solution(galaxies_map, column_count): # TODO this could use some refactoring
    # how tall is our matrix now after expanding?
    row_count = len(galaxies_map)

    # build up array of coordinates of galaxies
    galaxy_coords = []
    for idx,line in enumerate(galaxies_map):
        for galaxy in line:
            galaxy_coords.append(','.join([str(galaxy),str(idx)]))

    # build up array of all possible galaxy combos
    combos = []
    i = 0
    while i < len(galaxy_coords):
        z = i+1
        while z < len(galaxy_coords):
            combos.append([galaxy_coords[i], galaxy_coords[z]])
            z = z+1
        i = i+1

    # find the number of steps to get between galaxies for each combo
    steps = []
    for combo in combos:
        x1,y1 = combo[0].split(',')
        x2,y2 = combo[1].split(',')
        steps.append(abs(int(x2)-int(x1)) + abs(int(y2)-int(y1)))

    return sum(steps)

print("answer part 1:", get_solution(galaxies_map, column_count))

# part 2 - brute force-ish
superwide_map = []
million_dots = '.' * 999999 # 1000000-1 since the total dots is 1 million including the original dot
for line in lines_raw:
    new_line = line
    for column in columns_to_expand:
        new_line = new_line[:column] + million_dots + new_line[column:]
    superwide_map.append(new_line)

big_column_count = len(superwide_map[0])

big_galaxies_map = []
for line in superwide_map:
    line_galaxies = []
    p = re.compile("#")
    for m in p.finditer(line):
        line_galaxies.append(m.start())
    big_galaxies_map.append(line_galaxies)
    # expand vertically
    if line_galaxies == []: # if there's no galaxies in this line, expand by 1
        i = 0
        for i in range(0,999999):
            big_galaxies_map.append([])

print("answer part 2:", get_solution(big_galaxies_map, big_column_count))