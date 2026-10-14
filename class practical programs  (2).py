"""
Q5 - Word stemming using the Porter Stemmer algorithm (NLTK)

Setup (once, in Command Prompt / Terminal):   pip install nltk
The Porter Stemmer needs no extra NLTK data downloads.
Run in IDLE (F5).
"""
from collections import defaultdict
import re

try:
    from nltk.stem import PorterStemmer
    from nltk.tokenize import RegexpTokenizer
except ImportError:
    raise SystemExit("NLTK is not installed. Open Command Prompt and run:  pip install nltk")

WORDS = ["running", "runs", "runner", "ran", "easily", "easier", "caresses", "ponies",
         "cats", "studies", "studying", "studied", "connection", "connected",
         "connecting", "connections", "relational", "generalization", "happiness",
         "agreed", "agreement", "hopeful", "hopping", "hoping", "flies", "fairly",
         "computing", "computer", "computation", "computers"]

SENTENCE = ("The students were studying computational linguistics and connecting "
            "related ideas while their teachers were happily generalizing the results.")


def main():
    ps = PorterStemmer()

    print("=" * 50)
    print("1. STEMMING A LIST OF WORDS")
    print("=" * 50)
    print(f"{'Word':<18}{'Stem'}")
    print("-" * 36)
    for w in WORDS:
        print(f"{w:<18}{ps.stem(w)}")

    print("\n" + "=" * 50)
    print("2. WORDS GROUPED BY THEIR STEM")
    print("=" * 50)
    groups = defaultdict(list)
    for w in WORDS:
        groups[ps.stem(w)].append(w)
    for stem in sorted(groups):
        if len(groups[stem]) > 1:
            print(f"{stem:<12}<- {', '.join(groups[stem])}")

    print("\n" + "=" * 50)
    print("3. STEMMING A SENTENCE")
    print("=" * 50)
    tokens = RegexpTokenizer(r"\w+").tokenize(SENTENCE)
    stems = [ps.stem(t) for t in tokens]
    print("Original :", " ".join(tokens))
    print("Stemmed  :", " ".join(stems))

    print("\n" + "=" * 50)
    print("4. TRY YOUR OWN WORDS (blank line to quit)")
    print("=" * 50)
    while True:
        text = input("Enter word(s): ").strip()
        if not text:
            break
        for w in re.findall(r"[A-Za-z]+", text):
            print(f"  {w} -> {ps.stem(w)}")


if __name__ == "__main__":
    main()
