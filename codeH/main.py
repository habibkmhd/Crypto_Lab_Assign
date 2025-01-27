from src.encrypt import *

def main():
    # read and sanitize plaintext
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            plaintext = format_text(f.read(), SE)
            if len(plaintext) < PLAINTEXT_MIN_LENGTH:
                print(f"ERROR: Plaintext must be at least {PLAINTEXT_MIN_LENGTH} characters.")
                return
            if len(plaintext) > PLAINTEXT_MAX_LENGTH:
                print(f"ERROR: Plaintext must be at most {PLAINTEXT_MAX_LENGTH} characters.")
                return
    except FileNotFoundError:
        print(f"ERROR: {INPUT_FILE} not found.")
        return

    # write sanitized plaintext into file
    try:
        with open(PLAINTEXT_FILE, 'w', encoding='utf-8') as f:
            f.write(plaintext)
            print(f"Plaintext written to {PLAINTEXT_FILE}")
    except IOError:
        print(f"ERROR: Could not write to {PLAINTEXT_FILE}")
        return

    # read and validate key from file
    key = get_key(KEY_FILE, SE)
    if key is None:
        return
    if len(key) > KEY_MAX_LENGTH:
        print(f"ERROR: Key must be at most {KEY_MAX_LENGTH} characters.")
        return

    # Encrypt the plaintext
    ciphertext = encrypt(plaintext, key, SE)

    # Write the ciphertext
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(ciphertext)
            print(f"Ciphertext written to {OUTPUT_FILE}")
    except IOError:
        print(f"ERROR: Could not write to {OUTPUT_FILE}")
        return

if __name__ == "__main__":
    main()