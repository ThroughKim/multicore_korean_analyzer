
from collections import defaultdict

L1 = ['be', 'your']
L2 = ['the onion', 'be your self', 'great zoo', 'x men', 'corn day', 'yes be your self']

d = dict.fromkeys(L2)

for s, phrase in enumerate(L2):
    d[phrase] = defaultdict(int)
    for word1 in phrase.split(" "):
        for word2 in phrase.split(" "):
            if word1 in L1 and word2 in L1:
                output = word1, word2, phrase
                print(output)
                key = (word1, word2)
                d[phrase][key] += 1

print(d)
print(d['be your self'])
