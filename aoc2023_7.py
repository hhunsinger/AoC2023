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

card_types2 = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1,
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
    card_vals2 = []
    for card in hand:
        # count each type of card
        if not card_counts.get(card, None):
            card_counts[card] = hand.count(card)
        # record the val of each card, in order
        card_vals.append(card_types[card])
        card_vals2.append(card_types2[card])
    
    # analyze the hand type for part 1
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
    
    # analyze the hand type for part 2 # TODO refactor w/ part 1
    triples2 = 0
    pairs2 = 0
    hand_type2 = ''
    for card, count in card_counts.items():
        if card == 'J': # skip J at this part of the calculations
            continue
        else:
            if card_counts[card] == 5:
                hand_type2 = 'five_of_a_kind'
            elif card_counts[card] == 4:
                hand_type2 = 'four_of_a_kind'
            elif card_counts[card] == 3:
                triples2 = triples2 + 1
            elif card_counts[card] == 2:
                pairs2 = pairs2 + 1

    if not hand_type2:
        if triples2 == 1 and pairs2 == 1:
            hand_type2 = 'full_house'
        elif triples2 == 1 and pairs2 == 0:
            hand_type2 = 'three_of_a_kind'
        elif pairs2 == 2:
            hand_type2 = 'two_pair'
        elif pairs2 == 1:
            hand_type2 = 'one_pair'
        else:
            hand_type2 = 'high_card'
    
    # do special J calculations (assuming always exactly 5 cards in a hand)
    # if no J in hand, we've already calculated hand_type_2 above
    j_count = card_counts.get('J', None)
    if j_count:
        if j_count == 1:
            # full_house, five_of_a_kind not possible if 1 card is joker - not enough cards
            if hand_type2 == 'high_card': # JWXYZ
                hand_type2 = 'one_pair' # WWXYZ
            elif hand_type2 == 'one_pair': # JXXYZ
                hand_type2 = 'three_of_a_kind' # XXXYZ
            elif hand_type2 == 'two_pair': # JXXYY
                hand_type2 = 'full_house' # XXXYY
            elif hand_type2 == 'three_of_a_kind': # JXXXY
                hand_type2 = 'four_of_a_kind' # XXXXY
            elif hand_type2 == 'four_of_a_kind': # JXXXX
                hand_type2 = 'five_of_a_kind' # XXXXX
            
        elif j_count == 2:
            # two_pair, full_house, four_of_a_kind, five_of_a_kind are not possible if we have 2 jokers - not enough cards
            if hand_type2 == 'high_card': # JJXYZ
                hand_type2 = 'three_of_a_kind' # XXXYZ
            elif hand_type2 == 'one_pair': # JJXXY
                hand_type2 = 'four_of_a_kind' # XXXXY
            elif hand_type2 == 'three_of_a_kind': # JJXXX
                hand_type2 = 'five_of_a_kind' # XXXXX
            
        elif j_count == 3:
            # two_pair, three_of_a_kind, full_house, four_of_a_kind, five_of_a_kind are not possible if we have 3 jokers - not enough cards
            if hand_type2 == 'high_card': # JJJXY
                hand_type2 = 'four_of_a_kind' # XXXXY
            elif hand_type2 == 'one_pair': # JJJXX
                hand_type2 = 'five_of_a_kind' # XXXXX
        
        elif j_count == 4 or j_count == 5: # JJJJX or JJJJJ
            hand_type2 = 'five_of_a_kind'
        
    hands.append({
        'hand': hand,
        'bid': bid,
        'card_counts': card_counts,
        'hand_type': hand_type,
        'hand_type2': hand_type2,
        'card_vals': card_vals,
        'card_vals2': card_vals2
    })

# group by hand type
grouped_by_hand_type = {}
grouped_by_hand_type2 = {}
for type_name, type_rank in hand_types.items():
    # part 1
    grouped_by_hand_type[type_rank] = {}
    grouped_by_hand_type[type_rank]['unsorted'] = []
    # part 2
    grouped_by_hand_type2[type_rank] = {}
    grouped_by_hand_type2[type_rank]['unsorted'] = []
for hand in hands:
    # part 1
    grouped_by_hand_type[hand_types[hand['hand_type']]]['unsorted'].append(hand)
    # part 2
    grouped_by_hand_type2[hand_types[hand['hand_type2']]]['unsorted'].append(hand)

def insertion_sort(arr, puzzle_part): # thank you https://www.geeksforgeeks.org/python-program-for-insertion-sort/
    n = len(arr)  # Get the length of the array
    if n <= 1:
        return arr # If the array has 0 or 1 element, it is already sorted, so return
    for i in range(1, n):  # Iterate over the array starting from the second element
        key = arr[i]  # Store the current element as the key to be inserted in the right position
        j = i-1
        while j >= 0 and hand1_lt_hand2(key, arr[j], puzzle_part):  # Move elements greater than key one position ahead
            arr[j+1] = arr[j]  # Shift elements to the right
            j -= 1
        arr[j+1] = key  # Insert the key in the correct position
    return arr

def hand1_lt_hand2(hand1, hand2, puzzle_part):
    if puzzle_part == 1: # TODO should handle if puzzle_part isn't 1 or 2
        card_val_name = 'card_vals'
    elif puzzle_part == 2:
        card_val_name = 'card_vals2'
    # return True if hand 1 is less than hand 2
    # return False if hand 1 is greater than hand 2
    n = len(hand1[card_val_name]) # we're assuming hands are the same length, so we'll use this length for both
    for i in range(0, n):
        if hand1[card_val_name][i] == hand2[card_val_name][i]: # this position is equivalent; move to the next
            continue
        if hand1[card_val_name][i] < hand2[card_val_name][i]:
            return True
        if hand1[card_val_name][i] > hand2[card_val_name][i]:
            return False
    return False # if we got here, the hands are identical. the puzzle doesn't say how to handle that, so we'll just say hand 1 wins.

# sort each hand type group by high cards - part 1
for type_rank in grouped_by_hand_type.keys():
    grouped_by_hand_type[type_rank]['sorted'] = insertion_sort(grouped_by_hand_type[type_rank]['unsorted'], 1)
    grouped_by_hand_type2[type_rank]['sorted'] = insertion_sort(grouped_by_hand_type2[type_rank]['unsorted'], 2)

# do the final ranking (lowest index == weakest hand)
final_ranking = []
final_ranking2 = []
for i in range(1,len(hand_types)+1):
    for hand in grouped_by_hand_type[i]['sorted']:
        final_ranking.append(hand)
    for hand in grouped_by_hand_type2[i]['sorted']:
        final_ranking2.append(hand)

# calculate bids
def calculate_bids(foo):
    winnings = 0
    for idx, hand in enumerate(foo):
        rank = idx+1 # the index starts at zero but we want ranking to start at 1
        hand_winnings = rank * int(hand['bid'])
        winnings = winnings + hand_winnings
    return winnings

print("part 1 answer: ", calculate_bids(final_ranking))
print("part 2 answer: ", calculate_bids(final_ranking2))