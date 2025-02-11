from pycipher import Vigenere
import re
from itertools import permutations
from ngram_score import ngram_score

qgram = ngram_score("/home/halina/uni/Crypto_Lab_Assign/src/se_quadgrams.txt")
trigram = ngram_score("/home/halina/uni/Crypto_Lab_Assign/src/se_trigrams.txt")

ctext = 'sbjäacgazwvcbxddbfjmärmätävcbxacbdtttöipuftbjölägtfgdäerpctäsugmjsöågvijööcsböjmäwxdtfbstäsgödäärggzkvisxzlgqzfdoabörwtlhuöeioläägxuödbwvägvnvhtjöosxwmycphztytixuöeotbståyafdoabörwqzixsgöwmäucäthönvsmacäthtkcgäaxxäcoxsjloöyöwsydzmqriazcltoqxxvdääbsosämkfezzuovöphöxdzåxfnv'

KNOWN_KLEN = 10  # Set the known key length here
N = 100  # Number of best keys to keep

class nbest:
    def __init__(self, N):
        self.store = []
        self.N = N
    
    def add(self, item):
        self.store.append(item)
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]
    
    def __getitem__(self, k):
        return self.store[k]

    def __len__(self):
        return len(self.store)

rec = nbest(N)
for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ', 3):
    key = ''.join(i) + 'A' * (KNOWN_KLEN - len(i))
    pt = Vigenere(key).decipher(ctext)
    score = sum(trigram.score(pt[j:j+3]) for j in range(0, len(ctext), KNOWN_KLEN))
    rec.add((score, ''.join(i), pt[:30]))

next_rec = nbest(N)
for i in range(0, KNOWN_KLEN - 3):
    for k in range(N):
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ':
            key = rec[k][1] + c
            fullkey = key + 'A' * (KNOWN_KLEN - len(key))
            pt = Vigenere(fullkey).decipher(ctext)
            score = sum(qgram.score(pt[j:j+len(key)]) for j in range(0, len(ctext), KNOWN_KLEN))
            next_rec.add((score, key, pt[:30]))
    rec = next_rec
    next_rec = nbest(N)

bestkey = rec[0][1]
bestscore = qgram.score(Vigenere(bestkey).decipher(ctext))
for i in range(N):
    pt = Vigenere(rec[i][1]).decipher(ctext)
    score = qgram.score(pt)
    if score > bestscore:
        bestkey = rec[i][1]
        bestscore = score       

print(bestscore, 'Vigenere, known klen', KNOWN_KLEN, '"' + bestkey + '",', Vigenere(bestkey).decipher(ctext))
