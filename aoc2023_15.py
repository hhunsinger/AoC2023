# https://adventofcode.com/2023/day/15

import re

# test data
# solution part 1 = 1320
# solution part 2 = 145
input_raw = ['rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7']

# actual data
def load_input(file='private/aoc2023_15_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

input_raw = load_input()

steps = input_raw[0].split(',') # assuming input is only one line

def hash_algo(char, val):
    # Determine the ASCII code for the current character of the string.
    ascii_code = ord(char)
    # Increase the current value by the ASCII code you just determined.
    val = val + ascii_code
    # Set the current value to itself multiplied by 17.
    val = val * 17
    # Set the current value to the remainder of dividing itself by 256.
    val = val % 256
    return val

# part 1
current_vals = []
for step in steps:
    # Current value starts at 0
    current_val = 0
    for char in step:
        current_val = hash_algo(char, current_val)
    current_vals.append(current_val) # could just sum it up as we go, but maybe we'll need them later

print("answer part 1:", sum(current_vals)) # this was too easy

# part 2
boxes = []
for i in range(0,256):
    boxes.append([])

for step in steps:
    regex = '^(\w+?)([-=]{1})(\d?)$'
    match = re.search(regex,step)
    label = match.group(1)
    operator = match.group(2)
    focal_length = match.group(3)
    if focal_length:
        focal_length = int(focal_length)
    box = 0
    for char in label:
        box = hash_algo(char, box)
    if operator == '=':
        lens = {'label': label, 'focal_length': focal_length}
        found = False
        for idx,box_lens in enumerate(boxes[box]):
            if box_lens['label'] == label:
                found = True
                boxes[box][idx] = lens # replace this lens with the new lens
        if found == False:
            boxes[box].append(lens)
    elif operator == '-':
        for idx,box_lens in enumerate(boxes[box]):
            if box_lens['label'] == label:
                del boxes[box][idx] # remove this lens #TODO (can i do this? delete the element i'm iterating on?)

# calculate solution
lens_powers = []
for idy,box in enumerate(boxes):
    for idx,lens in enumerate(box):
        lens_power = 0
        # Multiply:
        # One plus the box number of the lens in question.
        lens_power = 1 + idy
        # The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
        lens_power = lens_power * (idx+1) # idx+1 = slot number of this lens
        # The focal length of the lens.
        lens_power = lens_power * lens['focal_length']
        lens_powers.append(lens_power) # could add it up as we go but this is easier to debug

print('answer part 2:', sum(lens_powers))
    