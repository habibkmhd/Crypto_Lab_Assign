import os
from math import sqrt
ALPHABET = 'abcdefghijklmnopqrstuvwxyzåäö'

 # Measures the likelihood that any two characters of a text are the same.
def index_of_coincidence(text):
    counts = [0]*29
    for char in text:
        counts[ALPHABET.index(char)] += 1
    numer = 0
    total = 0
    for i in range(29):
        numer += counts[i]*(counts[i]-1)
        total += counts[i]
    return 29*numer / (total*(total-1))

# We cut the text into slices where each slice contains every m_th letter
# and compute the IoC for each and average them. 
# Do this for many choices of m.
def do_slices_period(text):
    found = False
    period = 0
    while not found:
        period += 1
        slices = ['']*period
        for i in range(len(text)):
            slices[i%period] += text[i]
        sum = 0
        for i in range(period):
            sum += index_of_coincidence(slices[i])
        ioc = sum / period
        if ioc > 1.6:
        # with our formula a random text has an IoC ~=1 and Swedish text ~=1.68 (close to IoC of English)
            found = True
            return slices, period

# Prints out the expected key lengths for the TAs' texts
def find_klen(): 
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    for m in range(1,7):
    
        # STEP 1: load ciphertext 
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up two levels
        CIPHERTEXT_PATH = os.path.join(base_dir, f"ciphertext/{m}.crypto")
        
        with open(CIPHERTEXT_PATH, "r", encoding="utf-8") as f:
            ciphertext = f.read()
            
        # STEP 2: get key length using index of coincidence and slices
        slices, period = do_slices_period(ciphertext)
    
        print(f"ciphertext: {os.path.basename(CIPHERTEXT_PATH)}")
        print("expected key length: ",period)

