"""
Q4 - Finite-state machine for morphological parsing:
     generating the plural form of English nouns.
Run in IDLE (F5).

The machine reads the noun one letter at a time. Its state remembers the
information about the ENDING of the word that decides the plural rule.

State          Meaning (what the word ends with so far)     Plural rule
-------------  -------------------------------------------  ----------------
START          nothing read yet                             +s
VOWEL          a vowel (a, i, u, e, o after a vowel)        +s
CONS           an ordinary consonant                        +s
SIBILANT       s, x or z                                    +es
CH_SH          ch or sh                                     +es
Y_CONS         consonant + y   (city)                       y -> ies
Y_VOWEL        vowel + y       (boy)                        +s
O_CONS         consonant + o   (hero)                       +es
F              f                (leaf)                      f -> ves
FE             fe               (knife)                     fe -> ves

Irregular nouns (child, man, foot ...) and exceptions (photo, roof ...) are
handled by a small lexicon that is checked before the machine runs.
"""

VOWELS = set("aiu")
SIBILANTS = set("sxz")

IRREGULAR = {"child": "children", "man": "men", "woman": "women", "foot": "feet",
             "tooth": "teeth", "mouse": "mice", "goose": "geese", "person": "people",
             "ox": "oxen", "louse": "lice"}
UNCHANGED = {"sheep", "fish", "deer", "series", "species", "aircraft"}
EXCEPTIONS = {"photo": "photos", "piano": "pianos", "roof": "roofs", "chief": "chiefs",
              "belief": "beliefs", "safe": "safes", "cliff": "cliffs", "kilo": "kilos"}

VOWEL_LIKE = {"VOWEL", "O_CONS", "FE"}   # states whose last letter is a vowel


def next_state(state, ch):
    """Transition function of the finite-state machine."""
    if ch in SIBILANTS:
        return "SIBILANT"
    if ch == "c":
        return "C"
    if ch == "h":
        return "CH_SH" if state in ("C", "SIBILANT") else "CONS"
    if ch == "y":
        return "Y_VOWEL" if state in VOWEL_LIKE else "Y_CONS"
    if ch == "o":
        return "VOWEL" if state in VOWEL_LIKE else "O_CONS"
    if ch == "f":
        return "CONS" if state == "F" else "F"          # 'ff' -> ordinary ending
    if ch == "e":
        return "FE" if state == "F" else "VOWEL"
    if ch in VOWELS:
        return "VOWEL"
    return "CONS"                                        # every other letter


def run_machine(noun):
    state, path = "START", ["START"]
    for ch in noun:
        state = next_state(state, ch)
        path.append(state)
    return state, path


def apply_rule(noun, state):
    """Output function: build the plural from the final state."""
    if state in ("SIBILANT", "CH_SH", "O_CONS"):
        return noun + "es", "add 'es'"
    if state == "Y_CONS":
        return noun[:-1] + "ies", "change 'y' to 'ies'"
    if state == "F":
        return noun[:-1] + "ves", "change 'f' to 'ves'"
    if state == "FE":
        return noun[:-2] + "ves", "change 'fe' to 'ves'"
    return noun + "s", "add 's'"


def pluralize(noun):
    """Return (plural, rule description, state path)."""
    n = noun.lower().strip()
    if n in IRREGULAR:
        return IRREGULAR[n], "irregular noun (lexicon)", ["LEXICON"]
    if n in UNCHANGED:
        return n, "plural same as singular (lexicon)", ["LEXICON"]
    if n in EXCEPTIONS:
        return EXCEPTIONS[n], "exception to the rule (lexicon)", ["LEXICON"]
    state, path = run_machine(n)
    plural, rule = apply_rule(n, state)
    return plural, f"{rule}  [final state: {state}]", path


def morphological_parse(noun):
    """Two-level view: lexical form  <->  surface form."""
    plural, rule, _ = pluralize(noun)
    return f"{noun.lower()}+N+PL", plural


def main():
    nouns = ["cat", "dog", "bus", "box", "buzz", "church", "dish", "city", "baby",
             "boy", "key", "hero", "tomato", "photo", "piano", "leaf", "wolf", "knife",
             "wife", "roof", "cliff", "child", "man", "woman", "foot", "mouse",
             "tooth", "person", "sheep", "fish"]

    print("=" * 78)
    print("FSM PLURAL GENERATOR  (lexical form  ->  surface form)")
    print("=" * 78)
    print(f"{'Noun':<10}{'Lexical form':<16}{'Plural':<12}{'Rule applied'}")
    print("-" * 78)
    for n in nouns:
        lex, surface = morphological_parse(n)
        _, rule, _ = pluralize(n)
        print(f"{n:<10}{lex:<16}{surface:<12}{rule}")

    print("\nState trace for a few nouns:")
    for n in ["city", "church", "knife", "boy"]:
        _, _, path = pluralize(n)
        print(f"  {n:<8}: " + " \u2192 ".join(path))

    print("\n--- Enter your own nouns (blank line to quit) ---")
    while True:
        n = input("Noun: ").strip()
        if not n:
            break
        plural, rule, path = pluralize(n)
        print(f"  Plural : {plural}")
        print(f"  Rule   : {rule}")
        print("  Trace  : " + " \u2192 ".join(path) + "\n")


if __name__ == "__main__":
    main()
