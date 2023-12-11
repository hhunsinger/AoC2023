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
# valid chars 
# TODO is there a pattern here so we could define these programmatically? in a way that's easy to understand? I came up with this manually.
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
legend = {
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

# build up coordinate -> character map by parsing input data
chars_by_coords = {}
start = ''
for idy, line in enumerate(pipes_raw): # iterate thru lines
    for idx, char in enumerate(line): # iterate thru chars in the line to find the coords of each char
        coord_str = ','.join([str(idx), str(idy)])
        chars_by_coords[coord_str] = char # store characters by coordinate (look up chars by coords)

        # find the start (S) - this assumes only one S in the dataset
        if char == 'S':
            start = coord_str

def get_neighbor_coords(char, coords):
    '''
    Get a list of coordinates that are neighbors of character `char` at coordinates `coords`
    '''
    char_dirs = legend[char] # directions we can go from this character
    neighbor_coords = [] # init a list of neighbor coordinates
    (x,y) = coords.split(',')
    # iterate thru possible directions for this character and build up array of neighbor coords
    for dir in char_dirs.keys(): 
        # init a default None val to use if that direction is out of bounds
        neighbor_coord = { 
            'dir': dir, 
            'coords': None
        }
        match dir:
            case 'up': # TODO can we refactor these cases?
                up = int(y)-1
                if up < 0: up = None # out of bounds
                if up != None: 
                    neighbor_coord = { 
                        'dir': dir, 
                        'coords': ','.join([x,str(up)])
                    }
                    neighbor_coords.append(neighbor_coord)
                else:
                    neighbor_coords.append(neighbor_coord)
            
            case 'left':
                left = int(x)-1
                if left < 0: left = None
                if left != None: 
                    neighbor_coord = { 
                        'dir': dir,
                        'coords': ','.join([str(left),y])
                    }
                    neighbor_coords.append(neighbor_coord)
                else:
                    neighbor_coords.append(neighbor_coord)
            
            case 'down':
                down = int(y)+1
                if down > len(pipes_raw)-1: down = None
                if down != None: 
                    neighbor_coord = { 
                        'dir': dir,
                        'coords': ','.join([x,str(down)])
                    }
                    neighbor_coords.append(neighbor_coord)
                else:
                    neighbor_coords.append(neighbor_coord)

            case 'right':
                right = int(x)+1
                if right > len(pipes_raw[0])-1: right = None
                if right != None: 
                    neighbor_coord = { 
                        'dir': dir,
                        'coords': ','.join([str(right), y])
                    }
                    neighbor_coords.append(neighbor_coord)
                else:
                    neighbor_coords.append(neighbor_coord)
    return neighbor_coords

def is_valid_direction(start_char, next_char, direction_traveled):
    '''
    Function to see if pipe A (start_char) and pipe B (next_char) fit together, based
    on the definition in the legend. i.e. is this a valid direction to go?
    '''
    if legend[start_char].get(direction_traveled, None): # is this a direction we can travel from the start char?
        if next_char in legend[start_char][direction_traveled]: # is the next char a char we can travel to from the start char?
            return True
        else:
            return False
    else:
        return False

# vals to start our journey
char = 'S'
coords = start
prev_coords = ''
move_count = 0
done = False
while done != True: # and we're off
    move_count = move_count + 1 # increment move count
    neighbor_coords = get_neighbor_coords(char, coords) # get neighbor coordinates for the current char
    for neighbor_coord in neighbor_coords: # figure out which of the neighbors is one we can travel to
         
        # don't go backwards or out of bounds
        if neighbor_coord['coords'] == prev_coords or neighbor_coord['coords'] == None:
            continue 

         # what's the character at this neighbor coord?
        next_char = chars_by_coords[neighbor_coord['coords']]

        # we can never travel to a . char, so ignore it
        if next_char == '.':
            continue

        # check if we've reached the end of the loop
        if next_char == 'S':
            # we're back where we started!
            done = True # break out of the loop

        # is the next char fit with this char?
        is_valid_dir = is_valid_direction(char, next_char, neighbor_coord['dir'])

        # if so, set our starting values to this new char/coords so we move forward
        if is_valid_dir == True:
            prev_coords = coords
            char = next_char
            coords = neighbor_coord['coords']
            break # break out of this for loop and move back to the top of the while loop (i hope)

print('answer part 1:', int(move_count/2)) # we have a problem if it's not divisible by 2