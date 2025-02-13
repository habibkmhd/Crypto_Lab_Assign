from itertools import permutations
from src.decrypt import decrypt


# calculate Index of Coincidence (IC)
def calc_ic(text):
    freqs = {}
    for c in text:
        if c in freqs:
            freqs[c] += 1
        else:
            freqs[c] = 1

    n = len(text)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic

# estimate key length using Friedman-Test
def get_key_len(text, max_key_len=16):
    ics = []
    for key_len in range(1, max_key_len + 1):
        subgroups = [''.join(text[i::key_len]) for i in range(key_len)]

        ic_values = [calc_ic(sub) for sub in subgroups if len(sub) > 1]
        if ic_values:
            avg_ic = sum(ic_values) / len(ic_values)
            ics.append((key_len, avg_ic))
    
    return sorted(ics, key=lambda x: -x[1])[0][0]

# guess key using NGram analysis
def find_key(text, key_len, alphabet, trigram, qgram):
    key = ""
    best_score = float('-inf')

    # count trigrams
    for i in permutations(alphabet, 3):
        potential_key = ''.join(i) + 'A' * (key_len - len(i))
        pt = decrypt(text, potential_key, alphabet)
        score = sum(trigram.score(pt[i:i+3]) for i in range(0, len(text), key_len))

        if score > best_score:
            best_score = score
            key = ''.join(i)

    # count quadgrams
    n = len(key)
    while n < key_len:
        local_best_score = float('-inf')
        local_best_key = key

        for c in alphabet:
            new_key = key + c
            full_key = new_key + 'A' * (key_len - len(new_key))
            pt = decrypt(text, full_key, alphabet)
            new_score = sum(qgram.score(pt[i:i+len(new_key)]) for i in range(0, len(text), key_len))

            if new_score > local_best_score:
                local_best_score = new_score
                local_best_key = new_key

        key = local_best_key
        n += 1

    return key