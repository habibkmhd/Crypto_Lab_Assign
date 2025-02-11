from math import log10


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ'

class ngram_score:
    def __init__(self, ngramfile):
        self.ngrams = {}
        with open(ngramfile, 'r', encoding='utf-8') as f:  # Ensure correct encoding
            for line in f:
                key, count = line.strip().split(' ')
                if all(c in ALPHABET for c in key):  # Filter out unwanted n-grams
                    self.ngrams[key] = int(count)
        self.L = len(next(iter(self.ngrams)))  # Automatically detect n-gram length
        self.N = sum(self.ngrams.values())
        self.floor = log10(0.01 / self.N)

    def score(self, text):
        score = 0
        for i in range(len(text) - self.L + 1):
            ngram = text[i:i + self.L]
            if ngram in self.ngrams:
                score += log10(self.ngrams[ngram] / self.N)
            else:
                score += self.floor
        return score
