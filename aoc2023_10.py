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

# pipes_raw = load_input()

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


# build up coordinate / character maps
coords_by_char = []
chars_by_coords = []
start = {}
for idy, line in enumerate(pipes_raw): # iterate thru lines
    coords1 = {}
    coords2 = {}
    for idx, char in enumerate(line): # iterate thru chars in the line to find the coords of each char
        # store coordinates by character (look up coords by char)
        coords1 = {
            char: {
                'x': idx, # x coord is the index of this char in the line (starting with 0)
                'y': idy # y coord is the line number (starting with 0)
            }
        }
        coords_by_char.append(coords1)

        # find the start S
        if char == 'S': # this assumes only one S in the dataset
            start = coords1

        # store characters by coordinate (look up chars by coords)
        coord_str = ','.join([str(idx), str(idy)])
        coords2 = { coord_str: char }
        chars_by_coords.append(coords2)
print("coords by char:", coords_by_char)
print("chars_by_coords:", chars_by_coords)
print("start", start)


    # if char == 'S': # if this is the beginning, return all the possible directions
    #     return neighbor_coords
    # else: # otherwise, recursively move through the path
    #     neighbor_coords = follow_directions('S', start['S'], [])

def get_neighbor_coords(char, coords):
    char_dirs = legend[char]
    neighbor_coords = []
    for dir in char_dirs:
        match dir:
            case 'up':
                up = coords['y']-1
                if up < 0: up = None # TODO i think there's a better python syntax for this
                if up != None: 
                    neighbor_coords.append({ dir: ','.join([str(coords['x']),str(up)])})
                else:
                    neighbor_coords.append({ dir: None })
            
            case 'left':
                left = coords['x']-1
                if left < 0: left = None
                if left != None: 
                    neighbor_coords.append({ dir: ','.join(str(left),[str(coords['y'])])})
                else:
                    neighbor_coords.append({ dir: None })
            
            case 'down':
                down = coords['y']+1
                if down > len(pipes_raw)-1: down = None # TODO check for off by one
                if down != None: 
                    neighbor_coords.append({ dir: ','.join([str(coords['x']),str(down)])})
                else:
                    neighbor_coords.append({ dir: None })

            case 'right':
                right = coords['x']+1
                if right > len(pipes_raw[0])-1: right = None # TODO check for off by one
                if right != None: 
                    neighbor_coords.append({ dir: ','.join([str(right), str(coords['y'])])})
                else:
                    neighbor_coords.append({ dir: None })
    return neighbor_coords

neighbor_coords = get_neighbor_coords('S', start['S'])
print('neighbor coords', neighbor_coords)

# def follow_directions(char, coords, prev_neighbor_coords):
#     neighbor_coords = get_neighbor_coords(char, coords)
#     # check if the neighbor is valid (i.e. can connect to this piece)
#     for coords in neighbor_coords:

# def is_valid_direction(start_char, next_char, direction_traveled):
    

# create function is_valid_direction(start_char, next_char, direction_traveled)
#   in that function,
#   if next char is S, we've reached the end (could also check this before calling this function)
#   if next char is ., we it's automatically not valid (could also check this before calling this function)
#   compare chars to each other and see if they fit together in the direction they're stringed
# each char can only validly go in two directions. but don't go backwards, so it can only go one direction.
# so use is_valid_direction on all non-backwards directions to find the correct way to go
# need to use recursion because we don't know the path
# S can only go in 2 valid directions, so pick one randomly and start going thru the loop from there (using follow_directions()), ending in S


# for coords in neighbor_coords:
#     char = chars_by_coords[coords]
#     coords_arr = coords.split(',')
#     coords_dict = { 'x': coords_arr[0], 'y': coords_arr[1] }
#     follow_directions(char, coords_dict, neighbor_coords)

# TODO need to check if direction connects to this pipe
