import os

from src.decrypt import decrypt
from src.help_bc2 import do_slices_period

path = os.path.abspath(__file__)
path = os.path.dirname(path)

ALPHABET = 'abcdefghijklmnopqrstuvwxyzåäö'

for m in range(1,7):

    # STEP 1: load ciphertext 
    CIPHERTEXT_PATH = path + "/ciphertext/"+ str(m)+".crypto"
    with open(CIPHERTEXT_PATH, "r", encoding="utf-8") as f:
        ciphertext = f.read()
        
    # STEP 2: get key length using index of coincidence and slices

    slices, period = do_slices_period(ciphertext)

    print(f"ciphertext: {os.path.basename(CIPHERTEXT_PATH)}")
    print("expected key length: ",period)