from src.encrypt import *
#from src.decrypt import *

MODE = "encrypt"
LANG = "se"

# file paths
INPUT_FILE = "/home/halina/uni/Crypto_Lab_Assign/input.txt"
PLAINTEXT_FILE = "/home/halina/uni/Crypto_Lab_Assign/vig_group2.plain"
KEY_FILE = "/home/halina/uni/Crypto_Lab_Assign/vig_group2.key"
CIPHERTEXT_FILE = "/home/halina/uni/Crypto_Lab_Assign/vig_group2.crypto"

# length constraints
PLAINTEXT_MIN_LENGTH = 200
PLAINTEXT_MAX_LENGTH = 600
KEY_MAX_LENGTH = 16

def main():

    alphabet = Alphabet(LANG)

    # encryption
    if MODE == "encrypt":
        # read and sanitize plaintext
        try:
            with open(INPUT_FILE, 'r', encoding='utf-8') as f:
                plaintext = format_text(f.read(), alphabet)
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
        key = get_key(KEY_FILE, alphabet)
        if key is None:
            return
        if len(key) > KEY_MAX_LENGTH:
            print(f"ERROR: Key must be at most {KEY_MAX_LENGTH} characters.")
            return

        # encrypt plaintext by Vigenère cipher
        ciphertext = encrypt(plaintext, key, alphabet)

        # write ciphertext into file
        try:
            with open(CIPHERTEXT_FILE, 'w', encoding='utf-8') as f:
                f.write(ciphertext)
                print(f"Ciphertext written to {CIPHERTEXT_FILE}")
        except IOError:
            print(f"ERROR: Could not write to {CIPHERTEXT_FILE}")
            return

    # decryption
    elif MODE == "decrypt":
        pass

    # invalid mode
    else:
        print(f"ERROR: Invalid mode. Choose a mode between 'encrypt' and 'dencrypt'")
        return


if __name__ == "__main__":
    main()