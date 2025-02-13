from itertools import permutations
from src.decrypt import decrypt


# Calculate Index of Coincidence (IC) to estimate key length
def calc_ic(text):
    freqs = {}
    for c in text:
        freqs[c] = freqs.get(c, 0) + 1  # Count character frequencies

    n = len(text)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))  # Compute IC
    return ic

# Estimate key length using the Friedman test
def get_key_len(text, max_key_len):
    ics = []
    for key_len in range(1, max_key_len + 1):
        subgroups = [''.join(text[i::key_len]) for i in range(key_len)]  # Split text into key-length groups

        ic_values = [calc_ic(sub) for sub in subgroups if len(sub) > 1]  # Compute IC for each subgroup
        if ic_values:
            avg_ic = sum(ic_values) / len(ic_values)  # Compute average IC
            ics.append((key_len, avg_ic))
    
    return sorted(ics, key=lambda x: -x[1])[0][0]  # Return key length with highest IC

# Guess encryption key using n-gram analysis
def find_key(text, key_len, alphabet, trigram, qgram):
    key = ""
    best_score = float('-inf')

    # Try all trigrams in the alphabet as initial guesses for key
    for i in permutations(alphabet, 3):
        potential_key = ''.join(i) + 'A' * (key_len - len(i))  # Extend key with 'A'
        pt = decrypt(text, potential_key, alphabet)
        score = sum(trigram.score(pt[i:i+3]) for i in range(0, len(text), key_len))  # Score based on trigrams

        if score > best_score:
            best_score = score
            key = ''.join(i)

    # Expand key using quadgrams
    n = len(key)
    while n < key_len:
        local_best_score = float('-inf')
        local_best_key = key

        for c in alphabet:
            new_key = key + c  # Extend key with one more letter
            full_key = new_key + 'A' * (key_len - len(new_key))
            pt = decrypt(text, full_key, alphabet)
            new_score = sum(qgram.score(pt[i:i+len(new_key)]) for i in range(0, len(text), key_len))

            if new_score > local_best_score:
                local_best_score = new_score
                local_best_key = new_key

        key = local_best_key  # Update key with best candidate
        n += 1

    return key  # Return final key