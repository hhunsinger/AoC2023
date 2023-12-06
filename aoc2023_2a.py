# https://adventofcode.com/2023/day/2

# test data
# solution = 8
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

# The Elf would first like to know which games would have been possible if the bag contained 
# only 12 red cubes, 13 green cubes, and 14 blue cubes?

qualifying_games = []
for game_id in game_ids:
    rounds = games[game_id]
    disqualified = False
    for round in rounds:
        red = round.get('red', None)
        green = round.get('green', None)
        blue = round.get('blue', None)
        if red:
            if round['red'] > 12:
                disqualified = True
        if green:
            if round['green'] > 13:
                disqualified = True
        if blue:
            if round['blue'] > 14:
                disqualified = True
        if disqualified == True:
            break
    if disqualified == True:
        next
    else:
        qualifying_games.append(game_id)

print("part 1 answer:", sum(qualifying_games))
