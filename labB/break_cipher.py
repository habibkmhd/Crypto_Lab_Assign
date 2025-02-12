import os, sys
import re
from itertools import permutations
from src.ngram_score import ngram_score, ALPHABET
from src.friedman_test import calc_ic, est_key_len
from src.decrypt import decrypt

path = os.path.abspath(__file__)
path = os.path.dirname(path)

CIPHERTEXT_PATH = path + "/ciphertext/vig_group2.crypto"

QGRAM = ngram_score(path + "/letter_freqs/se_quadgrams.txt")
TRIGRAM = ngram_score(path + "/letter_freqs/se_trigrams.txt")

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
MAX_KEY_LEN = 16
N = 100

# STEP 1: load ciphertext and quadgram & trigram scores

with open(CIPHERTEXT_PATH, "r", encoding="utf-8") as f:
    ciphertext = f.read()

# STEP 2: get key length using Friedman-Test

key_len = est_key_len(ciphertext, MAX_KEY_LEN)

# STEP 3: break Vigenere cipher

candidates = []
for i in permutations(ALPHABET, 3):
    key = ''.join(i) + 'A' * (key_len - len(i))
    pt = decrypt(ciphertext, key, ALPHABET)
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
            pt = decrypt(ciphertext, fullkey, ALPHABET)
            new_score = sum(QGRAM.score(pt[j:j+len(new_key)]) for j in range(0, len(ciphertext), key_len))
            new_candidates.append((new_score, new_key, pt[:30]))
    new_candidates.sort(reverse=True, key=lambda x: x[0])
    candidates = new_candidates[:N]

bestkey = candidates[0][1]
bestscore = QGRAM.score(decrypt(ciphertext, bestkey, ALPHABET))
for score, key, _ in candidates:
    pt = decrypt(ciphertext, key, ALPHABET)
    new_score = QGRAM.score(pt)
    if new_score > bestscore:
        bestkey = key
        bestscore = new_score

print(f"ciphertext: {os.path.basename(CIPHERTEXT_PATH)}")
print(f"key lenth: {key_len}, key: {bestkey}")
print(f"decrypted text: {decrypt(ciphertext, bestkey, ALPHABET)}")