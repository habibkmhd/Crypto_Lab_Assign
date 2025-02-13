from math import log10

class NGram:
    def __init__(self, ngramfile, alphabet):
        self.ngrams = {}
        with open(ngramfile, 'r', encoding='utf-8') as f:
            for line in f:
                key, count = line.strip().split(' ')
                if all(c in alphabet for c in key):
                    self.ngrams[key] = int(count)
        self.n = len(next(iter(self.ngrams)))
        self.sum = sum(self.ngrams.values())
        self.default = log10(0.01 / self.sum)

    # calculate score of n-gram
    def score(self, text):
        score = 0
        for i in range(len(text) - self.n + 1):
            ngram = text[i:i + self.n]
            if ngram in self.ngrams:
                score += log10(self.ngrams[ngram] / self.sum)
            else:
                score += self.default
        return score