import re
from collections import Counter
import numpy as np
import random

# Define Swedish alphabet and character mapping
swedish_alphabet = "abcdefghijklmnopqrstuvwxyzåäö"
char_to_num = {char: i for i, char in enumerate(swedish_alphabet)}
num_to_char = {i: char for i, char in enumerate(swedish_alphabet)}

# Function to calculate Index of Coincidence (IC)
def index_of_coincidence(text):
    freq = Counter(text)
    N = len(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

# Function to estimate key length using IC
def estimate_key_length(ciphertext, max_key_length=16):
    ics = []
    for key_len in range(1, max_key_length + 1):
        subgroups = [''.join(ciphertext[i::key_len]) for i in range(key_len)]
        avg_ic = np.mean([index_of_coincidence(sub) for sub in subgroups if len(sub) > 1])
        ics.append((key_len, avg_ic))
    return sorted(ics, key=lambda x: -x[1])[0][0]  # Return the best key length

# Load quadgram statistics
def load_quadgrams(filename="/home/halina/uni/Crypto_Lab_Assign/src/se_quadgrams.txt"):
    quadgrams = {}
    total = 0
    with open(filename, "r") as f:
        for line in f:
            key, count = line.split()
            quadgrams[key] = int(count)
            total += int(count)
    if total == 0:
        raise ValueError("Quadgram file is empty or improperly formatted.")
    for key in quadgrams:
        quadgrams[key] = np.log10(quadgrams[key] / total)
    return quadgrams

# Score text based on quadgram probabilities
def quadgram_score(text, quadgrams):
    score = 0
    fallback_value = np.log10(0.01 / (len(quadgrams) + 1))  # Ensure a small fallback probability
    for i in range(len(text) - 3):
        quad = text[i:i+4]
        if quad in quadgrams:
            score += quadgrams[quad]
        else:
            score += fallback_value
    return score

# Hill-climbing approach to determine the best key
def determine_key(ciphertext, key_length, iterations=1000):
    quadgrams = load_quadgrams()
    key = ''.join(random.choice(swedish_alphabet) for _ in range(key_length))
    best_plaintext = decrypt_vigenere(ciphertext, key)
    best_score = quadgram_score(best_plaintext, quadgrams)
    
    for _ in range(iterations):
        new_key = list(key)
        new_key[random.randint(0, key_length - 1)] = random.choice(swedish_alphabet)
        new_key = ''.join(new_key)
        new_plaintext = decrypt_vigenere(ciphertext, new_key)
        new_score = quadgram_score(new_plaintext, quadgrams)
        
        if new_score > best_score:
            key, best_score, best_plaintext = new_key, new_score, new_plaintext
    
    return key

# Function to decrypt ciphertext
def decrypt_vigenere(ciphertext, key):
    key_nums = [char_to_num[k] for k in key]
    plaintext = ""
    for i, char in enumerate(ciphertext):
        decrypted_num = (char_to_num[char] - key_nums[i % len(key)]) % 29
        plaintext += num_to_char[decrypted_num]
    return plaintext

# Load and clean ciphertext
with open("/home/halina/uni/Crypto_Lab_Assign/ciphertext/vig_group6.crypto", "r", encoding="utf-8") as f:
    ciphertext = re.sub(r'[^a-zåäö]', '', f.read().lower())

# Estimate key length
key_length = estimate_key_length(ciphertext)
print(f"Estimated Key Length: {key_length}")

# Determine key using hill-climbing method
key = determine_key(ciphertext, key_length)
print(f"Recovered Key: {key}")

# Decrypt message
plaintext = decrypt_vigenere(ciphertext, key)
print("Decrypted Text:")
print(plaintext)
