# https://adventofcode.com/2023/day/19

import re

# test data
# solution part 1 = 19114
input_raw = [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
    '',
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}'
]

# actual data
def load_input(file='private/aoc2023_19_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

input_raw = load_input()

workflows_raw = []
parts_raw = []
for line in input_raw:
    # find the workflows -- any line that starts with a letter and isn't empty
    if re.search('^[a-z]+{', line):
        workflows_raw.append(line)
    elif line.startswith("{"):
        parts_raw.append(line)

workflows = {}
for line in workflows_raw:
    # example: px{a<2006:qkq,m>2090:A,rfg}
    # px = label
    # 1: if a < 2006, route to workflow qkq
    # 2: if m > 2090, route to A (accepted)
    # 3: route to workflow rfg

    match = re.search('^([a-z]+){([^}]+?)}$', line)
    label = match.group(1)
    workflow_raw = match.group(2)
    workflow = workflow_raw.split(',')
    workflows[label] = workflow

parts = []
for line in parts_raw:
    match = re.search('^{(.+?)}$', line)
    parts_str = match.group(1)
    parts_arr = parts_str.split(',')
    parts_dict = {}
    for part_foo in parts_arr:
        k,v = part_foo.split('=')
        parts_dict[k] = int(v)
    parts.append(parts_dict)

accepted = []
rejected = []
for part in parts:
    start = 'in'
    i = 0
    while True: # do the logic until we hit a break
        
        if start == 'A': # if we hit an A, this part is accepted and we stop processing
            accepted.append(part)
            break
        if start == 'R': # if we hit an R, this part is rejected and we stop processing
            rejected.append(part)
            break
        
        next = workflows[start][i]
        if ':' not in next: # if there's no : in the string, we're at a non-conditional workflow direction (usually at the end of a workflow)
            i = 0 # reset the workflow index
            start = next
            continue # do the next iteration of the while loop

        # if we get here, we're at a conditional workflow direction. parse it and process it.
        flow_parts = next.split(':')
        route = flow_parts[1] # where to go if the conditional is met
        match = re.search('^([xmas]{1})([<>]{1})(\d+)$',flow_parts[0])
        conditional_letter = match.group(1)
        conditional_operator = match.group(2)
        conditional_number = int(match.group(3))
        if conditional_operator == '>' and part[conditional_letter] > conditional_number: # maybe there's a more elegant way to do this
            start = route # our condition matches. move to new workflow and ignore the rest of this one
            i = 0 # reset the workflow index
            continue
        elif conditional_operator == '<' and part[conditional_letter] < conditional_number:
            start = route # our condition matches. move to new workflow and ignore the rest of this one
            i = 0 # reset the workflow index
            continue
        else:
            i = i+1 # the condition didn't match; move to the next step in this workflow
            continue # do the next iteration of the while loop
            # ideally there would be some error handling here so we don't flow forever if one of the conditions above isn't met

# tally up the solution
total = 0
for part in accepted:
    total = total + sum(part.values())

print("answer part 1:", total)