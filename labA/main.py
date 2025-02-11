from src.file import File
from src.encrypt import *

# languages: en, se
LANG = "se"

# file paths
INPUT_FILE = File("/home/halina/uni/Crypto_Lab_Assign/labA/input.txt")
KEY_FILE = File("/home/halina/uni/Crypto_Lab_Assign/labA/vig_group2.key")

PLAINTEXT_FILE = "/home/halina/uni/Crypto_Lab_Assign/labA/vig_group2.plain"
CIPHERTEXT_FILE = "/home/halina/uni/Crypto_Lab_Assign/labA/vig_group2.crypto"

# length constraints
MIN_PLAINTEXT_LEN = 200
MAX_PLAINTEXT_LEN = 600
MAX_KEY_LEN = 16


def main():

    # check if input text is empty
    if INPUT_FILE is None or not KEY_FILE.len:
        print(f"ERROR: Text is empty.")
        return

    # initialize alphabet
    alphabet = Alphabet(LANG)

    # check if key meets constraints
    key = KEY_FILE.content
    if KEY_FILE is None or not KEY_FILE.len:
        print(f"ERROR: Key is empty.")
        return
    if KEY_FILE.len > MAX_KEY_LEN:
        print(f"ERROR: Key must be at most {MAX_KEY_LEN} characters.")
        return
    if not KEY_FILE.check_chars(alphabet):
        print(f"ERROR: Key contains unsupported characters.")
        return

    # sanitize plaintext
    if INPUT_FILE.check_chars:
        plaintext = INPUT_FILE.sanitize_text(alphabet)
    else: 
        plaintext = INPUT_FILE.content

    # check if plaintext meets constraints
    if len(plaintext) < MIN_PLAINTEXT_LEN:
        print(f"ERROR: Plaintext must be at least {MIN_PLAINTEXT_LEN} characters.")
        return
    if len(plaintext) > MAX_PLAINTEXT_LEN:
        print(f"ERROR: Plaintext must be at most {MAX_PLAINTEXT_LEN} characters.")
        return

    # write sanitized plaintext into file
    try:
        with open(PLAINTEXT_FILE, 'w+', encoding='utf-8') as f:
            f.write(plaintext)
            print(f"Plaintext written to {PLAINTEXT_FILE}.")
    except IOError:
        print(f"ERROR: Could not write to {PLAINTEXT_FILE}.")
        return

    # encrypt plaintext using Vigenère cipher
    ciphertext = encrypt(plaintext, key, alphabet)

    # write ciphertext in file
    try:
        with open(CIPHERTEXT_FILE, 'w+', encoding='utf-8') as f:
            f.write(ciphertext)
            print(f"Ciphertext written to {CIPHERTEXT_FILE}.")
    except IOError:
        print(f"ERROR: Could not write to {CIPHERTEXT_FILE}.")
        return


if __name__ == "__main__":
    main()