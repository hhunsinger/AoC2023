# https://adventofcode.com/2023/day/5

import re

# test data
# solution part 1 = 35
# solution part 2 = 46
almanac_raw = [
    'seeds: 79 14 55 13',
    '',
    'seed-to-soil map:',
    '50 98 2',
    '52 50 48',
    '',
    'soil-to-fertilizer map:',
    '0 15 37',
    '37 52 2',
    '39 0 15',
    '',
    'fertilizer-to-water map:',
    '49 53 8',
    '0 11 42',
    '42 0 7',
    '57 7 4',
    '',
    'water-to-light map:',
    '88 18 7',
    '18 25 70',
    '',
    'light-to-temperature map:',
    '45 77 23',
    '81 45 19',
    '68 64 13',
    '',
    'temperature-to-humidity map:',
    '0 69 1',
    '1 0 69',
    '',
    'humidity-to-location map:',
    '60 56 37',
    '56 93 4'
]

# actual data
f = open("private/aoc2023_5_input.txt", "r")
almanac_raw = f.readlines()
f.close()

almanac = []
seeds = []
section_id = None
for line in almanac_raw:
    line = line.strip()
    if line == '':
        continue
    if ":" in line: # this is a header line
        if line.startswith("seeds: "):
            foo = line.split(": ")
            bar = foo[1].split()
            
            # part 1
            for seed in bar:
                seeds.append(int(seed))
            
            # part 2 
            seeds_list_last_index = len(seeds)-1
            seeds2 = []
            i = 0
            while i <= seeds_list_last_index:
                if (i % 2) == 0:
                    seeds2.append({'start_seed': seeds[i]})
                else:
                    most_recent_index = len(seeds2)-1
                    seeds2[most_recent_index]['end_seed'] = seeds2[most_recent_index]['start_seed'] + seeds[i] - 1
                i = i+1
            
        else:
            x = re.search("^(\w+)-\w+-(\w+) map:", line)
            sourcename = x.groups()[0]
            destname = x.groups()[1]
            almanac.append({'sourcename': sourcename, 'destname': destname, 'mappings': []})
            for idx, entry in enumerate(almanac):
                if entry['sourcename'] is sourcename:
                    section_id = idx
    else: # this is a mapping line
        [dest_start, source_start, range_length] = line.split()
        mapping = {
            'source_start': int(source_start), 
            'source_end': int(source_start) + int(range_length)-1,
            'dest_start': int(dest_start),
            'dest_end': int(dest_start) + int(range_length)-1,
        }
        almanac[section_id]['mappings'].append(mapping)
        
final_mappings = []

def process_mappings(sourcename, source):
    dest_num = None
    destname = None
    for category in almanac: # TODO is there a better way to get the right category than iterating thru all of them?
        if category['sourcename'] == sourcename:
            destname = category['destname']
            for mapping in category['mappings']:
                if mapping['source_start'] <= source <= mapping['source_end']:
                    diff = source - mapping['source_start']
                    dest_num = mapping['dest_start'] + diff
                    break
                
    if destname and not dest_num:
        dest_num = source

    # do the next level
    if not destname:
        return source # we've reached the end
    else:
        return process_mappings(destname, dest_num)
    
seed_locations = []
for seed in seeds:
    location = process_mappings('seed', seed)
    seed_locations.append(location)
    
print("part 1 answer:", min(seed_locations))

# part 2
seed_locations2 = []
for seed_range in seeds2:
    # this solution works but is brute force / not at all performant - 
    # took several hours to run with actual dataset. ranges would be 
    # better: start with lowest seed range, then find lowest dest 
    # range and see if any seeds match. then check next dest range 
    # until we find a dest range with a source range that matches.
    # then do the same thing with each dest. (untested algorithm idea)
    # hmm... actually i don't think that'll work because there's no 
    # guarantee that lowest source == lowest dest maybe if we go 
    # backwards and start with the lowest location range to see if 
    # there are any seeds that match in that range? the search could 
    # fan out very quickly though, might still not be performant
    # enough
    i = seed_range['start_seed']
    while i <= seed_range['end_seed']:
        location = process_mappings('seed', i)
        seed_locations2.append(location)
        i = i+1
    foo="bar"

print("part 2 answer", min(seed_locations2))

