# https://adventofcode.com/2023/day/15

# test data
# solution part 1 = 1320
input_raw = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

# actual data
def load_input(file='private/aoc2023_15_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

input_raw = load_input()

steps = input_raw[0].split(',') # assuming input is only one line
current_vals = []
for step in steps:
    # Current value starts at 0
    current_val = 0
    for char in step:
        # Determine the ASCII code for the current character of the string.
        ascii_code = ord(char)
        # Increase the current value by the ASCII code you just determined.
        current_val = current_val + ascii_code
        # Set the current value to itself multiplied by 17.
        current_val = current_val * 17
        # Set the current value to the remainder of dividing itself by 256.
        current_val = current_val % 256
    current_vals.append(current_val) # could just sum it up as we go, but maybe we'll need them later

print("answer part 1:", sum(current_vals)) # this was too easy