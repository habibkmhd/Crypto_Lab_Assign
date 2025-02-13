import os, sys
import re
from src.ngram import NGram
from src.key import calc_ic, get_key_len, find_key
from src.decrypt import decrypt

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
MAX_KEY_LEN = 16

path = os.path.abspath(__file__)
path = os.path.dirname(path)

CIPHERTEXT_PATH = path + "/ciphertext/vig_group2.crypto"

TRIGRAM = NGram(path + "/letter_freqs/se_trigrams.txt", ALPHABET)
QGRAM = NGram(path + "/letter_freqs/se_quadgrams.txt", ALPHABET)


def main():

    # STEP 1: load ciphertext
    with open(CIPHERTEXT_PATH, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    # STEP 2: estimate key length using Friedman-Test
    key_len = get_key_len(ciphertext, MAX_KEY_LEN)

    # STEP 3: guess key using NGram analysis
    key = find_key(ciphertext, key_len, ALPHABET, TRIGRAM, QGRAM)

    # STEP 4: decrypt ciphertext using key
    msg = decrypt(ciphertext, key, ALPHABET)

    print(f"ciphertext: {os.path.basename(CIPHERTEXT_PATH)}")
    print(f"key lenth: {key_len}, key: {key.lower()}")
    print(f"decrypted text: {msg.lower()}")


if __name__ == "__main__":
    main()