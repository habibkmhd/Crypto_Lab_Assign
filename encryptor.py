import re
import string

# Updated ALPHABET_MAPPING to include å, ä, ö
ALPHABET_MAPPING = {letter: index for index, letter in enumerate(string.ascii_lowercase)}
ALPHABET_MAPPING['å'] = 26
ALPHABET_MAPPING['ä'] = 27
ALPHABET_MAPPING['ö'] = 28

# Read content from files
with open('text.plain', 'r', encoding='utf-8') as file:
    TEXT = file.read()

with open('encr.key', 'r', encoding='utf-8') as file:
    KEY = file.read().strip()  # Strip any extra whitespace

# Create a reverse mapping
REVERSE_ALPHABET_MAPPING = {value: key for key, value in ALPHABET_MAPPING.items()}

def standarize_text(text):
    str = text.lower()
    print(str)
    str = re.findall('[a-zåäö]', str)
    return str

def get_encrypted_value(m, k):
    return (ALPHABET_MAPPING.get(m) + ALPHABET_MAPPING.get(k)) % 29

def encrypt(text, key):
    str = standarize_text(text)
    enc_key = standarize_text(key)
    encrypted_text = []
    
    for i in range(len(str)):
        j = i % len(enc_key)  # Use modulo to cycle through the key
        encrypted_value = get_encrypted_value(str[i], enc_key[j])
        encrypted_key = REVERSE_ALPHABET_MAPPING.get(encrypted_value)  # Use reverse mapping
        encrypted_text.append(encrypted_key)
    
    encrypted_text = "".join(encrypted_text)
    return encrypted_text

# Write the encrypted text to a .crypto file
with open('output.crypto', 'w', encoding='utf-8') as file:
    file.write(encrypt(TEXT, KEY))
