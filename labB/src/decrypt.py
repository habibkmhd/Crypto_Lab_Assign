# Decrypt ciphertext using a Vigenère cipher
def decrypt(text, key, alphabet):
    a2i = {a: i for i, a in enumerate(alphabet)}  # Map letters to indices
    i2a = {i: a for i, a in enumerate(alphabet)}  # Map indices to letters

    text = text.upper()  # Convert text to uppercase for consistency
    msg = ""
    for i, c in enumerate(text):
        if c in a2i:
            # Shift character backward based on key value
            msg += i2a[(a2i[c] - a2i[key[i % len(key)]]) % len(alphabet)]
        else:
            msg += c  # Preserve non-alphabet characters
    return msg