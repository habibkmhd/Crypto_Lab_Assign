from src.alphabet import Alphabet


# convert to lowercase and remove unsupported characters
def format_text(text, alphabet):
    text = text.lower()
    formatted = ''.join(c for c in text if c in alphabet.letters)
    if len(formatted) != len(text):
        print("WARNING: Unsupported characters were removed from the plaintext")
    return formatted

# read and validate key from file
def get_key(key_file, alphabet):
    try:
        with open(key_file, 'r', encoding='utf-8') as f:
            key = f.read().strip().lower()
            if not all(l in alphabet.letters for l in key):
                print(f"ERROR: Invalid characters.")
                return None
            return key
    except FileNotFoundError:
        print(f"ERROR: {key_file} not found")
        return None

# encrypt plaintext by Vigenère cipher
def encrypt(text, key, alphabet):
    ciphertext = ""
    key_len = len(key)

    for i, c in enumerate(text):
        key_c = key[i % key_len]
        encrypted_i = (alphabet.letters[c] + alphabet.letters[key_c]) % alphabet.n
        ciphertext += alphabet.reverse_dict[encrypted_i]

    return ''.join(ciphertext)