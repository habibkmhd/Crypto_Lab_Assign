import re
from itertools import permutations
from src.ngram_score import ngram_score, ALPHABET
from collections import Counter
import numpy as np

CIPHERTEXT_FILE = "/home/halina/uni/Crypto_Lab_Assign/labB/ciphertext/vig_group2.crypto"
QGRAM = ngram_score("/home/halina/uni/Crypto_Lab_Assign/labB/letter_freqs/se_quadgrams.txt")
TRIGRAM = ngram_score("/home/halina/uni/Crypto_Lab_Assign/labB/letter_freqs/se_trigrams.txt")
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ'

MAX_KEY_LEN = 16
N = 100

a2i = {ch: i for i, ch in enumerate(ALPHABET)}
i2a = {i: ch for i, ch in enumerate(ALPHABET)}

def decipher(text, key):
    text = text.upper()
    ret = ''
    for i, c in enumerate(text):
        if c in a2i:
            ret += i2a[(a2i[c] - a2i[key[i % len(key)]]) % 29]
        else:
            ret += c
    return ret  

# STEP 1: load ciphertext

with open(CIPHERTEXT_FILE, "r", encoding="utf-8") as f:
    ciphertext = f.read()

# STEP 2: estimate key length using Index of Coincidence (IC)

def calc_ic(text):
    freq = Counter(text)
    N = len(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

def estimate_key_len(ciphertext, max_key_length=16):
    ics = []
    for key_len in range(1, max_key_length + 1):
        subgroups = [''.join(ciphertext[i::key_len]) for i in range(key_len)]
        avg_ic = np.mean([calc_ic(sub) for sub in subgroups if len(sub) > 1])
        ics.append((key_len, avg_ic))
    return sorted(ics, key=lambda x: -x[1])[0][0]

key_len = estimate_key_len(ciphertext)

# STEP 3: break Vigenere cipher

candidates = []
for i in permutations(ALPHABET, 3):
    key = ''.join(i) + 'A' * (key_len - len(i))
    pt = decipher(ciphertext, key)
    score = sum(TRIGRAM.score(pt[j:j+3]) for j in range(0, len(ciphertext), key_len))
    candidates.append((score, ''.join(i), pt[:30]))
candidates.sort(reverse=True, key=lambda x: x[0])
candidates = candidates[:N]

for i in range(0, key_len - 3):
    new_candidates = []
    for score, key, _ in candidates:
        for c in ALPHABET:
            new_key = key + c
            fullkey = new_key + 'A' * (key_len - len(new_key))
            pt = decipher(ciphertext, fullkey)
            new_score = sum(QGRAM.score(pt[j:j+len(new_key)]) for j in range(0, len(ciphertext), key_len))
            new_candidates.append((new_score, new_key, pt[:30]))
    new_candidates.sort(reverse=True, key=lambda x: x[0])
    candidates = new_candidates[:N]

bestkey = candidates[0][1]
bestscore = QGRAM.score(decipher(ciphertext, bestkey))
for score, key, _ in candidates:
    pt = decipher(ciphertext, key)
    new_score = QGRAM.score(pt)
    if new_score > bestscore:
        bestkey = key
        bestscore = new_score

print(bestscore, 'Vigenere, known klen', key_len, '"' + bestkey + '",', decipher(ciphertext, bestkey))