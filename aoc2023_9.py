# https://adventofcode.com/2023/day/9

# test data
# solution part 1 = 114
# solution part 2 = 2
readings_raw = [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45',
]

# actual data
def load_input(file='private/aoc2023_9_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

readings_raw = load_input()

# parse input data
readings = []
for line in readings_raw:
    reading = []
    num_strs = line.split()
    for num_str in num_strs:
        reading.append(int(num_str))
    readings.append(reading)


# build up arrays of diffs for each row
def get_row_diffs(row):
    this_row_diffs = []
    for idx, num in enumerate(row):
        if idx+1 < len(row):
            this_row_diffs.append(row[idx+1] - row[idx]) # TODO abs?
    return this_row_diffs

diffs = []
for reading in readings:
    all_row_diffs = []
    all_row_diffs.append(reading)
    row_diffs = reading
    while sum(row_diffs) != 0:
        row_diffs = get_row_diffs(row_diffs)
        all_row_diffs.append(row_diffs)
    diffs.append(all_row_diffs)

# do predictions
for diff_arr in diffs:

    # part 1 - add prediction to the end of each row
    last_nonzero_diff_index = len(diff_arr)-2
    # even tho it's in the puzzle, for the purposes of this calculation, 
    # we don't need to append the end of the zero row and the last 
    # non-zero row with duplicate numbers, so we'll skip it
    i = last_nonzero_diff_index
    while i >= 1:
        last_val_this_row = diff_arr[i][len(diff_arr[i])-1] # get the last value of this diff array
        last_val_prev_row = diff_arr[i-1][len(diff_arr[i-1])-1] # get the last value of the previous diff array
        predicted_val = last_val_this_row + last_val_prev_row # get the predicted val for the previous row
        diff_arr[i-1].append(predicted_val)
        i = i-1
    
    # part 2 - add prediction to the beginning of each row
    i = last_nonzero_diff_index
    while i >= 1:
        first_val_this_row = diff_arr[i][0] # get the last value of this diff array
        first_val_prev_row = diff_arr[i-1][0] # get the last value of the previous diff array
        predicted_val = first_val_prev_row - first_val_this_row # get the predicted val for the previous row
        diff_arr[i-1].insert(0, predicted_val) # add the prediction to the beginning of the row
        i = i-1

# tally it up
total_part_1 = 0
total_part_2 = 0
for row in diffs:
    total_part_1 = total_part_1 + row[0][len(row[0])-1]
    total_part_2 = total_part_2 + row[0][0]

print("part 1 answer:", total_part_1)
print("part 2 answer:", total_part_2)

