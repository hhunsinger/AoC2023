# https://adventofcode.com/2023/day/7

# test data
# solution part 1 = 6440
hands_raw = [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483',
]

# actual data
f = open("private/aoc2023_7_input.txt", "r")
hands_raw = f.readlines()
f.close()

card_types = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'J': 10,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1,
}

hand_types = {
    'five_of_a_kind': 7,
    'four_of_a_kind': 6,
    'full_house': 5,
    'three_of_a_kind': 4,
    'two_pair': 3,
    'one_pair': 2,
    'high_card': 1
}

hands = []
for line in hands_raw:
    line = line.strip() # get rid of newline
    (hand, bid) = line.split()
    card_counts = {}
    card_vals = []
    for card in hand:
        # count each type of card
        if not card_counts.get(card, None):
            card_counts[card] = hand.count(card)
        # record the val of each card, in order
        card_vals.append(card_types[card])
    
    # analyze the hand
    triples = 0
    pairs = 0
    hand_type = ''
    for card, count in card_counts.items():
        if card_counts[card] == 5:
            hand_type = 'five_of_a_kind'
        elif card_counts[card] == 4:
            hand_type = 'four_of_a_kind'
        elif card_counts[card] == 3:
            triples = triples + 1
        elif card_counts[card] == 2:
            pairs = pairs + 1

    if not hand_type:
        if triples == 1 and pairs == 1:
            hand_type = 'full_house'
        elif triples == 1 and pairs == 0:
            hand_type = 'three_of_a_kind'
        elif pairs == 2:
            hand_type = 'two_pair'
        elif pairs == 1:
            hand_type = 'one_pair'
        else:
            hand_type = 'high_card' 
        
    hands.append({
        'hand': hand,
        'bid': bid,
        'card_counts': card_counts,
        'hand_type': hand_type,
        'card_vals': card_vals
    })

# group by hand type
grouped_by_hand_type = {}
for type_name, type_rank in hand_types.items():
    grouped_by_hand_type[type_rank] = {}
    grouped_by_hand_type[type_rank]['unsorted'] = []
for hand in hands:
    hand_type_id = hand_types[hand['hand_type']]
    grouped_by_hand_type[hand_type_id]['unsorted'].append(hand)

def insertion_sort(arr): # thank you https://www.geeksforgeeks.org/python-program-for-insertion-sort/
    n = len(arr)  # Get the length of the array
    if n <= 1:
        return arr # If the array has 0 or 1 element, it is already sorted, so return
    for i in range(1, n):  # Iterate over the array starting from the second element
        key = arr[i]  # Store the current element as the key to be inserted in the right position
        j = i-1
        while j >= 0 and hand1_lt_hand2(key, arr[j]):  # Move elements greater than key one position ahead
            arr[j+1] = arr[j]  # Shift elements to the right
            j -= 1
        arr[j+1] = key  # Insert the key in the correct position
    return arr

def hand1_lt_hand2(hand1, hand2):
    # return True if hand 1 is less than hand 2
    # return False if hand 1 is greater than hand 2
    n = len(hand1['card_vals']) # we're assuming hands are the same length, so we'll use this length for both
    for i in range(0, n):
        if hand1['card_vals'][i] == hand2['card_vals'][i]: # this position is equivalent; move to the next
            continue
        if hand1['card_vals'][i] < hand2['card_vals'][i]:
            return True
        if hand1['card_vals'][i] > hand2['card_vals'][i]:
            return False
    return False # if we got here, the hands are identical. the puzzle doesn't say how to handle that, so we'll just say hand 1 wins.

# sort each hand type group by high cards
for type_rank in grouped_by_hand_type.keys():
    grouped_by_hand_type[type_rank]['sorted'] = insertion_sort(grouped_by_hand_type[type_rank]['unsorted'])

# do the final ranking (lowest index == weakest hand)
final_ranking = []
for i in range(1,len(hand_types)+1):
    for hand in grouped_by_hand_type[i]['sorted']:
        final_ranking.append(hand)

# calculate bids
winnings = 0
for idx, hand in enumerate(final_ranking):
    rank = idx+1 # the index starts at zero but we want ranking to start at 1
    hand_winnings = rank * int(hand['bid'])
    winnings = winnings + hand_winnings

print("part 1 answer: ", winnings)