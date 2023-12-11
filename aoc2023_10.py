# https://adventofcode.com/2023/day/10

# test data

# solution part 1 = 4
pipes_raw = [
    '-L|F7',
    '7S-7|',
    'L|7||',
    '-L-J|',
    'L|-JF'
]

# solution part 1 = 8
pipes_raw = [
    '7-F7-',
    '.FJ|7',
    'SJLL7',
    '|F--J',
    'LJ.LJ'
]

# actual data
def load_input(file='private/aoc2023_10_input.txt'):
    with open(file, 'r') as myfile:
        input_array = myfile.read().splitlines()
    return input_array

pipes_raw = load_input()

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

# create a legend - map which directions you can go from each char
legend = {
    '|': ['up', 'down'],
    '-': ['right', 'left'],
    'L': ['up', 'right'],
    'J': ['up', 'left'],
    '7': ['down', 'left'],
    'F': ['down', 'right'],
    '.': [],
    'S': ['up', 'down', 'left', 'right'] # might not need to define this - there's only one and we'll treat it special
}

# create a legend - map which directions you can go from each char
# valid chars # TODO is there a pattern here so we could define these programmatically? in a way that's easy to understand?
# | / up = |,7,F
# | / down = |,L,J
# - / right = -, 7, J
# - / left = -, F, L
# L / up = |, F, 7
# L / right = -, J, 7
# J / up = |, F, 7
# J / left = -, L, F
# 7 / down = |, J, L
# 7 / left = -, F, L
# F / down = |, J, L
# F / right = -, J, 7
# S / up = |, F, 7
# S / down = |, J, L
# S / left = -, L, F
# S / right = -, J, 7
legend2 = {
    '|': {
            'up': ['|','7','F'],
            'down': ['|','L','J']
    },
    '-': {
            'right':['-','7','J'],
            'left':['-','F','L']
    } ,
    'L': {
            'up':['|','F','7'],
            'right':['-','J','7']
    },
    'J': {
            'up':['|','F','7'],
            'left':['-','L','F']
    },
    '7': {
            'down':['|','J','L'],
            'left':['-','F','L']
    },
    'F': {
            'down':['|','J','L'],
            'right':['-','J','7']
    },
    'S': {
            'up':['|','F','7'],
            'down':['|','J','L'],
            'left':['-','L','F'],
            'right':['-','J','7']
    },
    '.': {}
}

# build up coordinate / character map
chars_by_coords = {}
start = {}
for idy, line in enumerate(pipes_raw): # iterate thru lines
    coords = {}
    for idx, char in enumerate(line): # iterate thru chars in the line to find the coords of each char
        coord_str = ','.join([str(idx), str(idy)])
        chars_by_coords[coord_str] = char # store characters by coordinate (look up chars by coords)

        # find the start S
        if char == 'S': # this assumes only one S in the dataset
            start = coord_str

print("chars_by_coords:", chars_by_coords)
# print("start", start)

def get_neighbor_coords(char, coords):
    char_dirs = legend2[char]
    neighbor_coords = []
    (x,y) = coords.split(',')
    for dir in char_dirs.keys():
        foo = { # default val - will pass if that direction is out of bounds
            'dir': dir, 
            'coords': None
        }
        match dir: # TODO update based on new data structure
            case 'up':
                up = int(y)-1
                if up < 0: up = None # TODO i think there's a better python syntax for this
                if up != None: 
                    foo = { 
                        'dir': dir, 
                        'coords': ','.join([x,str(up)])
                    }
                    neighbor_coords.append(foo)
                else:
                    neighbor_coords.append(foo)
            
            case 'left':
                left = int(x)-1
                if left < 0: left = None
                if left != None: 
                    foo = { 
                        'dir': dir,
                        'coords': ','.join([str(left),y])
                    }
                    neighbor_coords.append(foo)
                else:
                    neighbor_coords.append(foo)
            
            case 'down':
                down = int(y)+1
                if down > len(pipes_raw)-1: down = None # TODO check for off by one
                if down != None: 
                    foo = { 
                        'dir': dir,
                        'coords': ','.join([x,str(down)])
                    }
                    neighbor_coords.append(foo)
                else:
                    neighbor_coords.append(foo)

            case 'right':
                right = int(x)+1
                if right > len(pipes_raw[0])-1: right = None # TODO check for off by one
                if right != None: 
                    foo = { 
                        'dir': dir,
                        'coords': ','.join([str(right), y])
                    }
                    neighbor_coords.append(foo)
                else:
                    neighbor_coords.append(foo)
    return neighbor_coords

def is_valid_direction(start_char, next_char, direction_traveled):
    if legend2[start_char].get(direction_traveled, None): # is this a direction we can travel from the start char?
        if next_char in legend2[start_char][direction_traveled]: # is the next char a char we can travel to from the start char?
            return True
        else:
            return False
    else:
        return False

def follow_directions(char, coords, neighbor_coords, prev_coords, move_count):
    move_count = move_count + 1
    new_char = None
    print("starting with", char)
    print("   prev coords", prev_coords)
    print("   all neighbor corods", neighbor_coords)
    for neighbor_coord in neighbor_coords:
        print("   this neighbor coords", neighbor_coord['coords'])
        if neighbor_coord['coords'] == prev_coords or neighbor_coord['coords'] == None: # don't go backwards or out of bounds
            print("     skipping - backwards")
            continue 
        start_char = char
        next_char = chars_by_coords[neighbor_coord['coords']]
        print("   evaluating next_char", next_char)
        print("   direction", neighbor_coord['dir'])
        if next_char == '.':
            print("     skipping - .")
            continue
        if next_char == 'S':
            # we've reached the end of the loop!
            print("done!")
            print("move count", move_count)
            print("answer part 1", move_count/2) # get the furthest point by dividing the moves in half
            return move_count # TODO check for off by 1
        is_valid_dir = is_valid_direction(start_char, next_char, neighbor_coord['dir'])
        print("   is valid dir", is_valid_dir)
        if is_valid_dir == True:
            new_char = next_char
            new_coords = neighbor_coord['coords']
            new_neighbor_coords = get_neighbor_coords(new_char, new_coords)
            print("  found valid direction - breaking")
            break # break out of this for loop and then recurse
    if not new_char:
        print("didn't find a valid route from here")
        return
    print("recursing")
    move_count = follow_directions(new_char, new_coords, new_neighbor_coords, coords, move_count)

neighbor_coords = get_neighbor_coords('S', start)
# print('neighbor coords', neighbor_coords)
move_count = follow_directions('S', start, neighbor_coords, None, 0) # no previous coords at the beginning
print("move count", move_count) # TODO why is it not bubbling up?