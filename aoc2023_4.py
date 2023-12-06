# https://adventofcode.com/2023/day/4

# test data
# solution part 1 = 13
# solution part 2 = 30
cards_raw = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
]

# real data
f = open("private/aoc2023_4_input.txt", "r")
cards_raw = f.readlines()
f.close()

cards = {}
card_ids = []
cards2 = []

# get rid of newlines at the end
for idx, card in enumerate(cards_raw):
    cards_raw[idx] = card.strip()

# parse raw cards data
for card in cards_raw:
    # get the card id
    foo = card.split(": ")
    bar = foo[0].split()
    card_id = int(bar[1])
    card_ids.append(card_id)
    # get the card numbers
    baz = foo[1].split(" | ")
    winning_nums = baz[0].split()
    card_nums = baz[1].split()
    # part 1 data format
    cards[card_id] = { "winning": set(winning_nums), "card_nums": set(card_nums) }
    # part 2 data format
    cards2.append({ "card_id": card_id, "winning": set(winning_nums), "card_nums": set(card_nums), "original": True })

for id in card_ids:
    winning_nums = cards[id]['winning']
    card_nums = cards[id]['card_nums']
    winners = card_nums.intersection(winning_nums)
    cards[id]['winners'] = list(winners)
    
     # part 1 data structure
    # score the card
    score = 0
    for winner in cards[id]['winners']:
        if score == 0: # first winner
            score = 1
        else:
            score = score * 2
    cards[id]['score'] = score
    
    # part 2 data structure
    for idx, card2 in enumerate(cards2):
        if card2['card_id'] == id:
            cards2[idx]['win_count'] = len(cards[id]['winners'])

score = 0
for id in card_ids:
    score = score + cards[id]['score']
    
print("part 1 answer: ", score)

# part 2

def copy_cards(card_id, num_copies):
    i = card_id + 1
    x = 1
    copies_to_make = []
    while x <= num_copies:
        copies_to_make.append(i)
        i = i+1
        x = x+1
    for copy_id in copies_to_make:
        how_many_copies = cards_count[card_id] # 1
        cards_count[copy_id] = cards_count[copy_id]+how_many_copies # increment the number of copies of this card

cards_count = {}
for id in card_ids:
    cards_count[id] = 1 # this is assuming all card IDs are unique

for card in cards2:
    copy_cards(card['card_id'], card['win_count'])

total_cards = 0
for card_id in card_ids:
    total_cards = total_cards + cards_count[card_id]
    
print("part 2 answer: ", total_cards)

