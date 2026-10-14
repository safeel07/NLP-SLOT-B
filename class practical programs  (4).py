"""
Q2 - Finite State Automaton that recognises strings ending with 'ab'
Alphabet : {a, b}
Run in IDLE (F5).

States
  q0 : start / last symbol was not the 'a' of an 'ab' ending
  q1 : last symbol read was 'a'
  q2 : last two symbols read were 'ab'  (ACCEPTING)
"""

STATES = ["q0", "q1", "q2"]
ALPHABET = {"a", "b"}
START = "q0"
ACCEPTING = {"q2"}

TRANSITIONS = {
    ("q0", "a"): "q1", ("q0", "b"): "q0",
    ("q1", "a"): "q1", ("q1", "b"): "q2",
    ("q2", "a"): "q1", ("q2", "b"): "q0",
}


def run_fsa(text):
    """Simulate the automaton. Returns (accepted, path, error)."""
    state = START
    path = [state]
    for ch in text:
        if ch not in ALPHABET:
            return False, path, f"'{ch}' is not in the alphabet {{a, b}}"
        state = TRANSITIONS[(state, ch)]
        path.append(state)
    return state in ACCEPTING, path, None


def show_table():
    print("Transition table")
    print("-" * 28)
    print(f"{'State':<10}{'a':<9}{'b':<9}")
    print("-" * 28)
    for s in STATES:
        label = ("->" if s == START else "  ") + ("*" if s in ACCEPTING else " ") + s
        print(f"{label:<10}{TRANSITIONS[(s, 'a')]:<9}{TRANSITIONS[(s, 'b')]:<9}")
    print("(-> start state, * accepting state)\n")


def test(text):
    accepted, path, err = run_fsa(text)
    print(f"Input : {text if text else '(empty string)'}")
    print("Path  : " + " \u2192 ".join(path))
    if err:
        print("Note  :", err)
    print("Result:", "Accepted" if accepted else "Rejected", "\n")


def main():
    print("FSA : strings over {a,b} that END WITH 'ab'\n")
    show_table()
    for s in ["ab", "aab", "abaab", "bab", "abb", "ba", "bbbb", "", "abca"]:
        test(s)
    print("--- Try your own strings (press Enter on a blank line to quit) ---")
    while True:
        s = input("Input string: ").strip()
        if not s:
            break
        test(s)


if __name__ == "__main__":
    main()
