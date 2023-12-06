# https://adventofcode.com/2023/day/6

# test data
# solution part 1 = 288
# solution part 2 = 
races_raw = [
    'Time:      7  15   30',
    'Distance:  9  40  200'
]

# this is small enough I'm just going to parse manually
races = [
    {'time': 7, 'distance': 9},
    {'time': 15, 'distance': 40},
    {'time': 30, 'distance': 200}
]

# actual data - paste in from private folder

win_counts = []
for race in races:
    # go thru each possible time and calculate the distance
    win_count = 0
    i = 1 # don't need to do 0 - it will never win
    while i <= race['time']:
        # each ms held increases by 1mm/ms
        # hold 1ms, goes 1mm/ms
        # hold 2ms, goes 2mm/ms, etc.
        speed = i
        time_left = race['time']-i
        distance = speed*time_left
        if distance > race['distance']:
            win_count = win_count+1
        i = i+1
    win_counts.append(win_count)

# print(win_counts)

# how many ways can you beat each race? multiply those values together and that's the part 1 answer
result = 1
for win_count in win_counts:
    result = result * win_count
print("part 1 answer:", result)

# part 2

# test data part 2
# solution = 71503
time2 = 71530
distance2 = 940200

# brute force isn't performant but it runs fast enough even with the real data (~1 min?)
win_count2 = 0
i = 1 # don't need to do 0 - it will never win
while i <= time2:
    speed = i
    time_left = time2-i
    distance = speed*time_left
    if distance > distance2:
        win_count2 = win_count2+1
    i = i+1
    
print("part 2 answer:", win_count2)
