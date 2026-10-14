"""
Q3 - Morphological analysis using NLTK
Covers: tokenization, stemming, lemmatization (with POS tags),
        WordNet base forms (morphy) and affix (prefix/suffix) analysis.

Setup (once, in Command Prompt / Terminal):   pip install nltk
The required NLTK data (wordnet, POS tagger) is downloaded automatically
the first time you run this program (internet needed for that one time).
Run in IDLE (F5).
"""
import re
import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet


def with_download(func, packages):
    """Run func(); if NLTK data is missing, download 'packages' and retry once."""
    try:
        return func()
    except LookupError:
        for p in packages:
            nltk.download(p, quiet=True)
        try:
            return func()
        except LookupError:
            return None


def heading(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


TEXT = ("The children were running quickly and playing happily in the beautiful gardens. "
        "The runners studied hard, and the bigger dogs were barking loudly.")

WORDS = ["running", "studies", "happily", "unhappiness", "children", "better",
         "wolves", "playing", "geese", "fairly", "reuse", "disagreement"]

PREFIXES = ["un", "re", "in", "im", "dis", "pre", "mis", "non", "over", "under"]
SUFFIXES = ["ation", "ment", "ness", "able", "ible", "less", "ful", "ing", "ize",
            "est", "ly", "ed", "er", "es", "s"]
AFFIX_RE = re.compile(
    r"^(?:(" + "|".join(PREFIXES) + r")(?=\w{3}))?"      # optional prefix
    r"(\w{3,}?)"                                         # stem (min 3 letters)
    r"(" + "|".join(SUFFIXES) + r")?$", re.I)            # optional suffix


def penn_to_wordnet(tag):
    return {"J": wordnet.ADJ, "V": wordnet.VERB,
            "N": wordnet.NOUN, "R": wordnet.ADV}.get(tag[0], wordnet.NOUN)


def tokenization(tokens):
    heading("1. TOKENIZATION")
    print("Text  :", TEXT)
    print("Tokens:", tokens)
    print("Total tokens:", len(tokens))


def stemming():
    heading("2. STEMMING (Porter vs Lancaster vs Snowball)")
    porter, lancaster, snowball = PorterStemmer(), LancasterStemmer(), SnowballStemmer("english")
    print(f"{'Word':<15}{'Porter':<15}{'Lancaster':<15}{'Snowball'}")
    print("-" * 60)
    for w in WORDS:
        print(f"{w:<15}{porter.stem(w):<15}{lancaster.stem(w):<15}{snowball.stem(w)}")


def lemmatization():
    heading("3. LEMMATIZATION (WordNet)")
    lem = WordNetLemmatizer()
    if with_download(lambda: lem.lemmatize("dogs"), ["wordnet", "omw-1.4"]) is None:
        print("WordNet data could not be downloaded. Check your internet connection.")
        return
    cases = [("running", "v"), ("running", "n"), ("children", "n"), ("better", "a"),
             ("better", "r"), ("wolves", "n"), ("geese", "n"), ("studies", "v"), ("was", "v")]
    print(f"{'Word':<12}{'POS':<6}{'Lemma'}")
    print("-" * 30)
    for w, p in cases:
        print(f"{w:<12}{p:<6}{lem.lemmatize(w, pos=p)}")
    print("\n(Lemmatization needs the part of speech: 'running' as a verb -> run, as a noun -> running)")


def morphy_base_forms():
    heading("4. WORDNET BASE FORMS (morphy)")
    test = ["dogs", "churches", "studies", "went", "better", "mice", "playing", "xyzs"]
    if with_download(lambda: wordnet.morphy("dogs"), ["wordnet", "omw-1.4"]) is None:
        print("WordNet data not available.")
        return
    print(f"{'Word':<12}{'Base form (morphy)'}")
    print("-" * 35)
    for w in test:
        print(f"{w:<12}{wordnet.morphy(w) or 'not found'}")


def affix_analysis():
    heading("5. AFFIX ANALYSIS (prefix + stem + suffix using regular expressions)")
    print(f"{'Word':<16}{'Prefix':<10}{'Stem':<12}{'Suffix'}")
    print("-" * 45)
    for w in WORDS:
        m = AFFIX_RE.match(w)
        pre, stem, suf = (m.group(1) or "-", m.group(2), m.group(3) or "-") if m else ("-", w, "-")
        print(f"{w:<16}{pre:<10}{stem:<12}{suf}")
    print("\n(Heuristic analysis: stems like 'happi' show spelling changes not undone.)")


def full_analysis(tokens):
    heading("6. FULL MORPHOLOGICAL ANALYSIS OF THE SENTENCE")
    tagged = with_download(lambda: nltk.pos_tag(tokens),
                           ["averaged_perceptron_tagger_eng", "averaged_perceptron_tagger"])
    if tagged is None:
        print("POS tagger data not available; skipping this section.")
        return
    porter, lem = PorterStemmer(), WordNetLemmatizer()
    print(f"{'Token':<12}{'POS':<6}{'Stem':<12}{'Lemma'}")
    print("-" * 42)
    for tok, tag in tagged:
        lemma = lem.lemmatize(tok.lower(), penn_to_wordnet(tag))
        print(f"{tok:<12}{tag:<6}{porter.stem(tok):<12}{lemma}")


def main():
    tokens = RegexpTokenizer(r"\w+").tokenize(TEXT)   # needs no extra NLTK data
    tokenization(tokens)
    stemming()
    lemmatization()
    morphy_base_forms()
    affix_analysis()
    full_analysis(tokens)


if __name__ == "__main__":
    main()
