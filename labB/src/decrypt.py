# decrypt ciphertext by using key
def decrypt(text, key, alphabet):
    a2i = {a: i for i, a in enumerate(alphabet)}
    i2a = {i: a for i, a in enumerate(alphabet)}

    text = text.upper()
    msg = ""
    for i, c in enumerate(text):
        if c in a2i:
            msg += i2a[(a2i[c] - a2i[key[i % len(key)]]) % len(alphabet)]
        else:
            msg += c

    return msg