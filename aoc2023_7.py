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
# f = open("private/aoc2023_7_input.txt", "r")
# hands_raw = f.readlines()
# f.close()

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
    for card in hand:
        if not card_counts.get(card, None):
            card_counts[card] = hand.count(card)
    
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
        if triples == 1 and pairs == 2:
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
        'hand_type': hand_type
    })

print(hands)

# NOT YET DONE

# TODO
# - rank by hand type, then by high card (starting with first card in hand)
# - calculate bid values (bid * rank)
# - add together bid values