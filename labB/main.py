import os
import re
from src.ngram import NGram
from src.key import calc_ic, get_key_len, find_key
from src.decrypt import decrypt

# Define the alphabet used in encryption
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
MAX_KEY_LEN = 16  # Maximum key length for decryption

# Get the absolute path of the current file and define the ciphertext file path
path = os.path.abspath(__file__)
path = os.path.dirname(path)
CIPHERTEXT_PATH = path + "/ciphertext/vig_group2.crypto"

# Load n-gram frequency models for trigrams and quadgrams
TRIGRAM = NGram(path + "/letter_freqs/se_trigrams.txt", ALPHABET)
QGRAM = NGram(path + "/letter_freqs/se_quadgrams.txt", ALPHABET)

def main():
    # STEP 1: Load the ciphertext from the file
    with open(CIPHERTEXT_PATH, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    # STEP 2: Estimate key length using the Friedman test
    key_len = get_key_len(ciphertext, MAX_KEY_LEN)

    # STEP 3: Guess the encryption key using n-gram analysis
    key = find_key(ciphertext, key_len, ALPHABET, TRIGRAM, QGRAM)

    # STEP 4: Decrypt the ciphertext using the discovered key
    msg = decrypt(ciphertext, key, ALPHABET)

    # Print results
    print(f"ciphertext: {os.path.basename(CIPHERTEXT_PATH)}")
    print(f"key length: {key_len}, key: {key.lower()}")
    print(f"decrypted text: {msg.lower()}")

if __name__ == "__main__":
    main()