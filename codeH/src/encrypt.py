import string

# file paths
INPUT_FILE = "input.txt"
PLAINTEXT_FILE = "vig-group2.plain"
KEY_FILE = "vig-group2.key"
OUTPUT_FILE = "vig-group2.crypto"

# length constraints
PLAINTEXT_MIN_LENGTH = 200
PLAINTEXT_MAX_LENGTH = 600
KEY_MAX_LENGTH = 16

# alphabet-values mapping
LETTERS = {letter: i for i, letter in enumerate(string.ascii_lowercase)}

# Swedish alphabet
SE = LETTERS.copy()
SE['å'] = 26
SE['ä'] = 27
SE['ö'] = 28

# convert to lowercase and remove unsupported characters
def format_text(text, letters):
    text = text.lower()
    formatted = ''.join(c for c in text if c in letters)
    if len(formatted) != len(text):
        print("WARNING: Unsupported characters were removed from the plaintext")
    return formatted

# read and validate key from file
def get_key(key_file, letters):
    try:
        with open(key_file, 'r', encoding='utf-8') as f:
            key = f.read().strip().lower()
            if not all(l in letters for l in key):
                print(f"ERROR: Invalid characters.")
                return None
            return key
    except FileNotFoundError:
        print(f"ERROR: {key_file} not found")
        return None

# encrypt plaintext by Vigenère cipher
def encrypt(text, key, letters):
    REVERSE_LETTERS = {i: letter for letter, i in letters.items()}
    ciphertext = ""
    key_len = len(key)

    for i, c in enumerate(text):
        key_c = key[i % key_len]
        encrypted_i = (letters[c] + letters[key_c]) % len(letters)
        ciphertext += REVERSE_LETTERS[encrypted_i]

    return ''.join(ciphertext)