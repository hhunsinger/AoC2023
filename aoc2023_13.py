# https://adventofcode.com/2023/day/13

import re

# test data
# solution part 1 = 405
input_raw = [
    '#.##..##.',
    '..#.##.#.',
    '##......#',
    '##......#',
    '..#.##.#.',
    '..##..##.',
    '#.#.##.#.',
    '',
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#'
]

# actual data
def load_input(file='private/aoc2023_13_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

input_raw = load_input()

patterns = []
this_pattern = []
for line in input_raw:
    if line != '':
        this_pattern.append(line)
    else:
        patterns.append(this_pattern)
        this_pattern = []
# grab the last pattern, which doesn't have an empty line after it to trigger saving it to `patterns`
patterns.append(this_pattern) 

horizontal_scores = []
vertical_scores = []
for idz, pattern in enumerate(patterns):
    # look for vertical symmetry (symmetry between rows)
    # first find two identical rows
    # go row by row and compare to the next one to see if it's the same
    possible_match_row_indices = []
    for idx,row in enumerate(pattern):
        if idx < len(pattern)-1: # can't compare to the next if we're at the last one # TODO check for off by 1
            if row == pattern[idx+1]: # we have a match!
                possible_match_row_indices.append(idx)
    
    # then check rows above/below to see if they match, stopping when we get to the top or bottom
    # if you reach two mis-matched rows but haven't reached the end - this isn't symmetry! look for it elsewhere in the pattern
    distance = 1
    symmetrical = None
    for x in possible_match_row_indices:
        symmetrical = True # assume symmetrical till proven otherwise
        if x == 0: # handle first row matches special - only 1 row in this case, and it's always a mirror so we don't need to check the rest
            horizontal_scores.append(1)
            break
        before_index = x
        after_index = x
        while before_index >= 0 and after_index < (len(pattern)-1):
            before_index = x - distance
            if before_index < 0: # we've gotten to the top so we're done
                break

            after_index = x + distance + 1 # add 1 for the row directly on the other side of the center line
            if before_index >= 0 and after_index < len(pattern):
                if pattern[before_index] == pattern[after_index]: # we're still in symmetry. continue.
                    distance = distance + 1
                else:
                    # this possible match is a bust. move to the next possible match.
                    symmetrical = False
                    break
        if symmetrical == True:
            horizontal_scores.append(x+1) # the number of rows above the midline is the index of this possible match plus 1 (since arrays start at 0)
            break # assuming we don't have 2 lines of symmetry. (is that even possible?)

    # if we haven't found symmetry yet, look for horizontal symmetry (symmetry between columns)
    # let's do a little trick where we turn the matrix on its side (90 degrees clockwise) -- convert columns 
    # to rows -- and then use the same algorithm as above    

    if possible_match_row_indices == [] or horizontal_scores == [] or symmetrical == False:
        rotated_pattern = []
        for y in range(0,len(pattern[0])):
            rotated_row = ''
            for x in range(0,len(pattern)):
                rotated_row = pattern[x][y] + rotated_row
            rotated_pattern.append(rotated_row)
        
        # now we can repeat the same algorithm we used for vertical symmetry #TODO refactor this! should be a function not copypasta

        # first find two identical rows
        # go row by row and compare to the next one to see if it's the same
        possible_match_row_indices = []
        for idx,row in enumerate(rotated_pattern):
            if idx < len(rotated_pattern)-1: # can't compare to the next if we're at the last one # TODO check for off by 1
                if row == rotated_pattern[idx+1]: # we have a match!
                    possible_match_row_indices.append(idx)

        # then check rows above/below to see if they match, stopping when we get to the top or bottom
        # if you reach two mis-matched rows but haven't reached the end - this isn't symmetry! look for it elsewhere in the pattern
        distance = 1
        symmetrical = None
        for x in possible_match_row_indices:
            symmetrical = True
            if x == 0: # handle first row matches special - only 1 row in this case, and it's always a mirror so we don't need to check the rest
                vertical_scores.append(1)
                break
            before_index = x
            after_index = x
            while before_index >= 0 and after_index < (len(rotated_pattern)-1):
                before_index = x - distance
                if before_index < 0: # we've gotten to the top so we're done
                    break

                after_index = x + distance + 1 # add 1 for the row directly on the other side of the center line
                if before_index >= 0 and after_index < len(rotated_pattern):
                    if rotated_pattern[before_index] == rotated_pattern[after_index]: # we're still in symmetry. continue.
                        distance = distance + 1
                    else:
                        # this possible match is a bust. move to the next possible match.
                        symmetrical = False
                        break
            if symmetrical == True:
                vertical_scores.append(x+1) # the number of rows above the midline is the index of this possible match plus 1 (since arrays start at 0)
                break # assuming we don't have 2 lines of symmetry. (is that even possible?)

print("solution part 1:", sum([(sum(horizontal_scores)*100), sum(vertical_scores)]))