import os
import re
import random
from src.ngram import NGram
from src.key import calc_ic, get_key_len, find_key
from src.decrypt import decrypt
from src.klen import find_klen

# Define the alphabet used in encryption
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
MAX_KEY_LEN = 16  # Maximum key length for decryption

# Get the absolute path of the current file and define the ciphertext file path
path = os.path.abspath(__file__)
path = os.path.dirname(path)
# To decrypt texts from students:
n = random.choice([2,3,5,6,7,9,10,12,17,18,19,24]) #choose a text at random to decrypt
CIPHERTEXT_PATH = path + "/ciphertext/vig_group"+str(n)+".crypto"

# To decrypt texts from the TAs (replace the line 'key_len =  est_key_len(ciphertext, MAX_KEY_LEN)' by 'key_len = 123')
# since we found by 'klen.py' that the key_len should be 123
# now we also found that the key is 'HÄRPRESENTERARUPPSALAUNIVERSITETFORSKKINGMEDUTGÅNGSPUNKTFRÅNENAVUNIVERSITETETSMESTBERÖMDAPROFESSORERGENOMTIDERNACARLVONLINN'
# so we can skip everything and directly go to 'msg = decrypt(ciphertext, key, ALPHABET)' with 'bestkey' the key above
#m=random.choice([1,2,3,4,5,6])
#CIPHERTEXT_PATH = path + "/ciphertext/"+ str(m)+".crypto"

# Load n-gram frequency models for trigrams and quadgrams
TRIGRAM = NGram(path + "/letter_freqs/se_trigrams.txt", ALPHABET)
QGRAM = NGram(path + "/letter_freqs/se_quadgrams.txt", ALPHABET)

def main():
    # STEP 1: Load the ciphertext from the file
    with open(CIPHERTEXT_PATH, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    # STEP 2: Estimate key length using the Friedman test
    key_len = get_key_len(ciphertext, MAX_KEY_LEN)
    # If decrypting TAs' texts, use: 
    #find_klen() #prints the expected key lengths for the 6 texts
    #key_len = 123   # Half of them have the same expected key length 

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
