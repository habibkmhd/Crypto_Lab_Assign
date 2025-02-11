class File:
    def __init__(self, filepath):
        try :
            with open(filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.len = len(self.content)
        except FileNotFoundError:
            print(f"ERROR: {filepath} not found.")
            return None

    # lower characters and remove unsupported characters from text
    def sanitize_text(self, alphabet):
        self.content = self.content.lower()
        self.content = ''.join(c for c in self.content if c in alphabet.letters)
        if len(self.content) != self.len:
            print("WARNING: Unsupported characters were removed from the plaintext")
        return self.content

    # check if text contains unsupported characters
    def check_chars(self, alphabet):
        return all(l in alphabet.letters for l in self.content)