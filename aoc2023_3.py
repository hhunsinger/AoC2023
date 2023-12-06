# https://adventofcode.com/2023/day/3

# test data
# answer part 1: 4361
# answer part 2: 467835
schematic = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]

# answer part 1: 413
# answer part 2: 6756
schematic = [
    '12.......*..',
    '+.........34',
    '.......-12..',
    '..78........',
    '..*....60...',
    '78..........',
    '.......23...',
    '....90*12...',
    '............',
    '2.2......12.',
    '.*.........*',
    '1.1.......56'
]

# answer part 1 = 925
# answer part 2 = 6756
schematic = [
    '12.......*..',
    '+.........34',
    '.......-12..',
    '..78........',
    '..*....60...',
    '78.........9',
    '.5.....23..$',
    '8...90*12...',
    '............',
    '2.2......12.',
    '.*.........*',
    '1.1..503+.56'
]

# answer part 1 = 62
schematic = [
    '.......5......',
    '..7*..*.....4*',
    '...*13*......9',
    '.......15.....',
    '..............',
    '..............',
    '..............',
    '..............',
    '..............',
    '..............',
    '21............',
    '...*9.........'
]

# real data
f = open("private/aoc2023_3_input.txt", "r")
schematic = f.readlines()
f.close()

special_chars = '`~!@#$%^&*()_+-=[]\{}|;\':",/<>?'
# actually, these are the only special chars in the data set:
# special_chars = ['#', '+', '/', '*', '&', '-', '=', '$', '@', '%']

line_metadata = {}
line_ids = []

# strip newlines
for idx, line in enumerate(schematic):
    schematic[idx] = line.strip()

all_numbers = []
qualifying_numbers = []
current_number = ""
num_started = False
qualifying_num_flag = False
possible_gears = []

# part 2 - get possible gears
for idx, line in enumerate(schematic):
    for char_id, char in enumerate(line):
        if char == '*':
            possible_gears.append({"x": idx, "y": char_id, "numbers": [] })

# parse input into proper data structure            
num_tracker = ''
for idx, line in enumerate(schematic):
    line_ids.append(idx)
    line_metadata[idx] = {}
    line_metadata[idx]['numbers'] = []
    for char_id, char in enumerate(line):
        if char.isnumeric():
            num_tracker = num_tracker + char
        else:
            if num_tracker: # we just finished a number
                num_length = len(num_tracker)
                number = {
                    'index' : char_id-num_length,
                    'number' : int(num_tracker),
                    'length' : num_length
                }
                line_metadata[idx]['numbers'].append(number)
                num_tracker = ''
    
    # see if we're still tracking a number at the end of a line
    if num_tracker: # we just finished a number
        num_length = len(num_tracker)
        number = {
            'index' : len(line)-num_length,
            'number' : int(num_tracker),
            'length' : num_length
        }
        line_metadata[idx]['numbers'].append(number)
        num_tracker = ''

qualifying_numbers = []

# TODO refactor: create function that takes x and y coords and checks if there's a special char there
for id in line_ids:
    prev_line = ""
    next_line = ""
    if id-1 >= 0:
        prev_line = schematic[id-1]
    if id+1 <= max(line_ids):
        next_line = schematic[id+1]
    for number in line_metadata[id]['numbers']:
        # check the char before
        index_of_char_before_number = number['index']-1
        if index_of_char_before_number >= 0:
            if schematic[id][number['index']-1] in special_chars:
                qualifying_numbers.append(number['number'])
                if schematic[id][number['index']-1] == '*':
                    for gear in possible_gears:
                        if gear['x'] == id and gear['y'] == index_of_char_before_number:
                            gear['numbers'].append(number['number'])
                continue # so we don't dupe if there are special chars elsewhere adjacent

        # check the char after
        index_of_char_after_number = number['index'] + number['length']
        if index_of_char_after_number <= len(schematic[id])-1:
            if schematic[id][index_of_char_after_number] in special_chars:
                qualifying_numbers.append(number['number'])
                if schematic[id][index_of_char_after_number] == '*':
                    for gear in possible_gears:
                        if gear['x'] == id and gear['y'] == index_of_char_after_number:
                            gear['numbers'].append(number['number'])
                continue

        # check all chars above
        if prev_line:
            # immediately above, 1 before, and 1 after
            i = number['index']-1
            if i < 0: # don't do a negative index
                i = 0
            qualified = False
            while i <= (number['length'])+number['index']:
                if i > len(prev_line)-1: # don't go past the end of the line
                    break
                if prev_line[i] in special_chars:
                    if qualified == False:
                        qualifying_numbers.append(number['number'])
                        qualified = True
                    if prev_line[i] == '*':
                        for gear in possible_gears:
                            if gear['x'] == id-1 and gear['y'] == i:
                                gear['numbers'].append(number['number'])
                i = i + 1
            if qualified:
                qualified = False
                continue

        # check all chars below
        if next_line:
            # immediately below, 1 before, and 1 after
            i = number['index']-1
            if i < 0: # don't do a negative index
                i = 0
            qualified = False
            while i <= (number['length'])+number['index']:
                if i > len(next_line)-1: # don't go past the end of the line
                    break
                if next_line[i] in special_chars:
                    if qualified == False:
                        qualifying_numbers.append(number['number'])
                        qualified = True
                    if next_line[i] == '*':
                        for gear in possible_gears:
                            if gear['x'] == id+1 and gear['y'] == i:
                                gear['numbers'].append(number['number'])
                i = i + 1
            if qualified:
                qualified = False
                continue

# part 2
gear_ratios = []
for gear in possible_gears:
    if len(gear['numbers']) == 2:
        gear_ratios.append(gear['numbers'][0]*gear['numbers'][1])

print("answer part 1:", sum(qualifying_numbers))
print("answer part 2:", sum(gear_ratios))