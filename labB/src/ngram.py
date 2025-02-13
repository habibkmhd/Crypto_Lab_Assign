from math import log10

# NGram class for scoring text based on n-gram frequencies
class NGram:
    def __init__(self, ngramfile, alphabet):
        self.ngrams = {}
        with open(ngramfile, 'r', encoding='utf-8') as f:
            for line in f:
                key, count = line.strip().split(' ')
                if all(c in alphabet for c in key):
                    self.ngrams[key] = int(count)
        self.n = len(next(iter(self.ngrams)))  # Determine n-gram length
        self.sum = sum(self.ngrams.values())  # Compute total n-gram occurrences
        self.default = log10(0.01 / self.sum)  # Default score for unknown n-grams

    # Score a given text using n-gram frequency analysis
    def score(self, text):
        score = 0
        for i in range(len(text) - self.n + 1):
            ngram = text[i:i + self.n]
            if ngram in self.ngrams:
                score += log10(self.ngrams[ngram] / self.sum)  # Log probability of known n-gram
            else:
                score += self.default  # Default score for unknown n-grams
        return score