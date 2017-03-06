from itertools import combinations_with_replacement

L1 = ['b', 'c', 'd', 'e', 't', 'w', 'x', 'y', 'z']
L2 = ['the onion', 'be your self', 'great zoo', 'x men', 'corn day']

phrase_map = {}

for phrase in L2:
    word_count = {word: phrase.count(word) for word in L1 if word in phrase}

    occurrence_map = {}
    for x, y in combinations_with_replacement(word_count, 2):
        occurrence_map[(x,y)] = occurrence_map[(y,x)] = \
            word_count[x] * word_count[y]

    phrase_map[phrase] = occurrence_map

print phrase_map
