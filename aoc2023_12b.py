# https://adventofcode.com/2023/day/12 - Part 2
# DO NOT RUN THIS!!!!!

import itertools
import re

# test data
# solution part 1 = 21
# solution part 2 = 525152
input_raw = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1'
]

# actual data
def load_input(file='private/aoc2023_12_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

# input_raw = load_input()

rows = []
for line in input_raw:
    all_springs, broken_springs = line.split()
    rows.append ({'all_springs': all_springs, 'broken_springs': broken_springs.split(',')})

# part 2
# "unfold" the records (expand 5x, separate by ?'s)
# brute force - this will take a while...
big_rows = []
for row in rows:
    all_springs = (row['all_springs'] + '?') * 5
    broken_springs = []
    for i in range(0,5):
        broken_springs = broken_springs + row['broken_springs']
    big_row = {'all_springs': all_springs, 'broken_springs': broken_springs}
    big_rows.append(big_row)

def permute(chars,rep):
    # thank you https://stackoverflow.com/questions/45990454/generating-all-possible-combinations-of-characters-in-a-string
    yield from itertools.product(*([chars] * rep)) 

# brute force - don't run this because it can't even get through the test data without crashing XD
counts = []
for row in big_rows:    
    # first find all sets of question marks, and their location in the string
    q_mark_sets = []
    q_mark_regex = '([\?]+?)[^\?]*'
    matches = re.finditer(q_mark_regex, row['all_springs'])
    for match in matches:
        q_mark_sets.append({'start': match.start(), 'length': len(match.groups(0)[0])})

    # then find all possible permutations of the question marks
    # for example, for '???' permutations are: ... ### #.. ##. .## ..# #.# .#.
    for idx,q_mark_set in enumerate(q_mark_sets):
        q_mark_sets[idx]['permutations'] = []
        for x in permute('.#', q_mark_set['length']):
            q_mark_sets[idx]['permutations'].append(''.join(x))

    # then find all possible permutations of the row by putting the ? permutation strings back in place
    row_possibilities = []
    foo = row['all_springs']
    # change question marks in the list, set by set:
    # - create list of permutations with just question mark set 0 changed
    # - iterate thru that list and create new list of permutations with set 1 changed
    # - repeat, set 2, etc
    
    permutations = {}
    # seed the list of permutations from the first set of question marks for this row
    permutations[0] = []
    for q_permutation in q_mark_sets[0]['permutations']:
        # substring replace
        # new_line = new_line[:column] + '.' + new_line[column:]
        foo = foo[:q_mark_sets[0]['start']] + q_permutation + foo[q_mark_sets[0]['start']+q_mark_sets[0]['length']:]
        permutations[0].append(foo)

    # now do the same thing for remaining question mark sets
    for idx,q_mark_set in enumerate(q_mark_sets): # TODO refactor with above?
        if idx == 0: continue # we already did the first set
        permutations[idx] = []
        for q_permutation in q_mark_set['permutations']: # go thru all permutations of this question mark set
            for bar in permutations[idx-1]: # apply it to the permutations for the previous question mark set
                foo = bar[:q_mark_set['start']] + q_permutation + bar[q_mark_set['start']+q_mark_set['length']:]
                permutations[idx].append(foo) # save it to a new set of permutations
    
    # we only care about the last set of permutations
    final_permutations = permutations[len(q_mark_sets)-1] 

    # then compare all row permutations to the regex, counting how many match
    count = 0
    regex_str = '^\.*?#{' + '}\.+?#{'.join(row['broken_springs']) + '}\.*?$'
    for permutation in final_permutations:
        match = re.search(regex_str,permutation)
        if match is not None: 
            count = count + 1
    counts.append(count) # could just count them all as we're going and not keep track of individual row counts, but this is clearer

print("answer part 2: ", sum(counts))