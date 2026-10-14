"""
Section 2 - Deterministic Finite Automata (DFA) Simulator
Run in IDLE (F5). Keep 'dfa.txt' in the same folder.
The DFA can be loaded from the file OR typed in manually.
"""
import os


class DFA:
    def __init__(self, states, alphabet, transitions, initial, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions      # {(state, symbol): next_state}
        self.initial = initial
        self.finals = finals

    # ---- check that the description is a proper (complete) DFA ----
    def validate(self):
        errors = []
        if self.initial not in self.states:
            errors.append(f"Initial state '{self.initial}' is not in the state set.")
        for f in self.finals:
            if f not in self.states:
                errors.append(f"Final state '{f}' is not in the state set.")
        for (s, a), t in self.transitions.items():
            if s not in self.states or t not in self.states:
                errors.append(f"Transition ({s},{a})->{t} uses an unknown state.")
            if a not in self.alphabet:
                errors.append(f"Transition symbol '{a}' is not in the alphabet.")
        for s in self.states:
            for a in self.alphabet:
                if (s, a) not in self.transitions:
                    errors.append(f"Missing transition for ({s},{a}).")
        return errors

    def print_table(self):
        print("\nTransition Table")
        print("-" * (10 + 8 * len(self.alphabet)))
        print(f"{'State':<10}" + "".join(f"{a:<8}" for a in self.alphabet))
        print("-" * (10 + 8 * len(self.alphabet)))
        for s in self.states:
            mark = ("->" if s == self.initial else "  ") + ("*" if s in self.finals else " ")
            print(f"{mark + s:<10}" + "".join(f"{self.transitions[(s, a)]:<8}" for a in self.alphabet))
        print("(-> initial state, * final state)\n")

    def run(self, text):
        """Return (accepted, path, error_message)."""
        state = self.initial
        path = [state]
        for ch in text:
            if ch not in self.alphabet:
                return False, path, f"symbol '{ch}' is not in the alphabet"
            state = self.transitions[(state, ch)]
            path.append(state)
        return state in self.finals, path, None


def load_from_file(filename):
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    states = alphabet = initial = None
    finals, transitions, inputs = [], {}, []
    section = None
    with open(fpath, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            low = line.lower()
            if low.startswith("states:"):
                states = [x.strip() for x in line.split(":", 1)[1].split(",")]
            elif low.startswith("alphabet:"):
                alphabet = [x.strip() for x in line.split(":", 1)[1].split(",")]
            elif low.startswith("initial:"):
                initial = line.split(":", 1)[1].strip()
            elif low.startswith("final:"):
                finals = [x.strip() for x in line.split(":", 1)[1].split(",")]
            elif low.startswith("transitions"):
                section = "t"
            elif low.startswith("inputs"):
                section = "i"
            elif section == "t":
                s, a, t = [x.strip() for x in line.split(",")]
                transitions[(s, a)] = t
            elif section == "i":
                inputs.append(line)
    return DFA(states, alphabet, transitions, initial, finals), inputs


def read_manually():
    states = [s.strip() for s in input("States (comma separated, e.g. q0,q1,q2): ").split(",")]
    alphabet = [a.strip() for a in input("Alphabet (e.g. a,b): ").split(",")]
    initial = input("Initial state: ").strip()
    finals = [s.strip() for s in input("Final state(s) (comma separated): ").split(",")]
    transitions = {}
    print("Enter the transition table:")
    for s in states:
        for a in alphabet:
            transitions[(s, a)] = input(f"  delta({s}, {a}) = ").strip()
    return DFA(states, alphabet, transitions, initial, finals)


def simulate(dfa, text):
    accepted, path, err = dfa.run(text)
    shown = text if text else "(empty string)"
    print(f"Input           : {shown}")
    print("Transition Path : " + " \u2192 ".join(path))
    if err:
        print(f"Note            : {err}")
    print("Result          : " + ("Accepted" if accepted else "Rejected") + "\n")
    return accepted


def main():
    print("DFA SIMULATOR")
    print("1. Load DFA from file (dfa.txt)")
    print("2. Enter DFA manually")
    choice = input("Choose 1 or 2 [1]: ").strip() or "1"

    file_inputs = []
    if choice == "2":
        dfa = read_manually()
    else:
        dfa, file_inputs = load_from_file("dfa.txt")

    errors = dfa.validate()
    if errors:
        print("\nInvalid DFA description:")
        for e in errors:
            print("  -", e)
        return

    print("\nStates   :", ", ".join(dfa.states))
    print("Alphabet :", ", ".join(dfa.alphabet))
    print("Initial  :", dfa.initial)
    print("Final    :", ", ".join(dfa.finals))
    dfa.print_table()

    acc = rej = 0
    if file_inputs:
        print("=" * 55)
        print("Simulating input strings from file")
        print("=" * 55)
        for s in file_inputs:
            if simulate(dfa, s):
                acc += 1
            else:
                rej += 1
        print(f"Summary -> Accepted: {acc} | Rejected: {rej}\n")

    print("--- Enter your own strings (press Enter on a blank line to quit) ---")
    while True:
        s = input("Input string: ").strip()
        if not s:
            break
        simulate(dfa, s)


if __name__ == "__main__":
    main()
