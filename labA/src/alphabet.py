import string

class Alphabet:
    def __init__(self, lang="en"):
        self.letters = {letter: i for i, letter in enumerate(string.ascii_lowercase)}

        self.lang = lang
        if lang == "en":
            pass
        if lang == "se":
            self.letters['å'] = 26
            self.letters['ä'] = 27
            self.letters['ö'] = 28
        else:
            print(f"ERROR: Invalid language")
            return

        self.reverse_dict = {i: letter for letter, i in self.letters.items()}
        self.n = len(self.letters)


if __name__ == "__main__":
    swedish_alphabet = Alphabet('se')
    print(swedish_alphabet.letters)