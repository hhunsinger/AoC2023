# https://adventofcode.com/2023/day/14

# test data
# solution part 1 = 136
input_raw = [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....'
]

# actual data
def load_input(file='private/aoc2023_14_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

input_raw = load_input()

# roll all the rocks to the north (top of input)

# actually, let's rotate the map clockwise so columns become rows - easier to work with rows than across columns
rotated_input = []
for y in range(0,len(input_raw[0])):
    rotated_row = ''
    for x in range(0,len(input_raw)):
        rotated_row = input_raw[x][y] + rotated_row
    rotated_input.append(rotated_row)

# now we want to roll to the right instead of to the top
rolled_input = []
for row in rotated_input:
    new_line = ''
    row_sections = row.split('#')
    for ids, section in enumerate(row_sections):
        new_section = ''
        max_place = len(section)-1
        # count the number of O's in this section
        O_count = section.count('O')
        # starting at the end, place O's until we run out
        i = max_place
        while i >= 0:
            if O_count == 0: # we're out of O's, so prepend with .
                new_section = '.'+new_section
            else: # we've still got O's left; prepend with O
                new_section = 'O'+new_section
                O_count = O_count-1
            i = i-1
        # add back the stationary rock that was removed from the split
        if ids != 0: # we don't want to add an extra rock to the beginning of the line
            new_section = '#' + new_section 
        new_line = new_line + new_section
    rolled_input.append(new_line)

# calculate the weight of each column (not row - because we're rotated clockwise)
z = 0
scores = []
while z <= len(rolled_input[0])-1: # go thru all indexes of the row
    count = 0
    i = 0    
    while i <= len(rolled_input)-1: # go thru all indexes of the column
        if rolled_input[i][z] == 'O': # if it's a O, count it
            count = count+1
        score = count * (z+1) # the score is the weight (which is the column index+1) times the number of O's
        i = i+1
    scores.append(score)
    z = z+1
    
print("answer part 1:", sum(scores))