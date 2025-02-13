from math import sqrt
ALPHABET = 'abcdefghijklmnopqrstuvwxyzåäö'


 # measures the likelihood that any two characters of a text are the same.
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

# we cut the text into slices where each slice contains every m_th letter
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
        

