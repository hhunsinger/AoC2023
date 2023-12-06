# https://adventofcode.com/2023/day/2

# test data
# solution = 2286
games_raw = [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'
]

# real data
f = open("private/aoc2023_2_input.txt", "r")
games_raw = f.readlines()
f.close()

games = {}
game_ids = []
for game in games_raw:
    foo = game.split(': ')
    # get game id
    bar = foo[0].split(' ')
    game_id = int(bar[1])
    game_ids.append(game_id)
    # get games
    rounds = []
    rounds_raw = foo[1].split('; ')
    for round_raw in rounds_raw:
        colors_raw = round_raw.split(", ")
        colors = {}
        for color_raw in colors_raw:
            baz = color_raw.split(' ')
            colors[baz[1].replace("\n", '')] = int(baz[0])
        rounds.append(colors)
    games[game_id] = rounds


# what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

minimum_cubes_games = {}
sum_powers = 0
for game_id in game_ids:
    red_min = 0
    green_min = 0
    blue_min = 0
    for round in games[game_id]:
        red = round.get('red', None)
        green = round.get('green', None)
        blue = round.get('blue', None)
        if red:
            if round['red'] > red_min:
                red_min = round['red']
        if green:
            if round['green'] > green_min:
                green_min = round['green']
        if blue:
            if round['blue'] > blue_min:
                blue_min = round['blue']
    power = red_min * green_min * blue_min
    minimum_cubes_games[game_id] = {
        'red': red_min,
        'green': green_min,
        'blue': blue_min,
        'power': power
    }
    sum_powers = sum_powers + power

print("part 2 answer:", sum_powers)