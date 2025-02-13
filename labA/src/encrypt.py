# encrypt plaintext by Vigenère cipher
def encrypt(text, key, alphabet):
    ciphertext = ""
    key_len = len(key)

    for i, c in enumerate(text):
        key_c = key[i % key_len]
        encrypted_i = (alphabet.letters[c] + alphabet.letters[key_c]) % alphabet.n
        ciphertext += alphabet.reverse_dict[encrypted_i]

    return ''.join(ciphertext)