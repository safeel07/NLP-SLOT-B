"""
Section 3 - Smart Pattern Matching Engine (Regular Expressions)
Run in IDLE (F5). Keep 'text_data.txt' in the same folder.
"""
import re
import os

DATE_RE    = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-](?:\d{4}|\d{2})\b")
PHONE_RE   = re.compile(r"(?<![\d])(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)")
HASHTAG_RE = re.compile(r"(?<!\w)#\w+")
MENTION_RE = re.compile(r"(?<![\w.])@\w+")


def load_text(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, encoding="utf-8") as f:
        return f.read()


def show(title, matches):
    print(f"\n--- {title} ---")
    if matches:
        for i, m in enumerate(matches, 1):
            print(f"  {i}. {m}")
    else:
        print("  No matches found.")
    print(f"Total matches: {len(matches)}")


def search_pattern(text, regex):
    return [m.group() for m in regex.finditer(text)]


def search_word(text, word):
    pat = re.compile(rf"\b{re.escape(word)}\b", re.I)
    return search_with_context(text, pat)


def search_prefix(text, prefix):
    pat = re.compile(rf"\b{re.escape(prefix)}\w*", re.I)
    return search_pattern(text, pat)


def search_suffix(text, suffix):
    pat = re.compile(rf"\w*{re.escape(suffix)}\b", re.I)
    return search_pattern(text, pat)


def search_with_context(text, pat):
    """Return the lines that contain the pattern, with line numbers."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if pat.search(line):
            out.append(f"(line {n}) {line.strip()}")
    return out


def menu():
    print("\n" + "=" * 42)
    print("   SMART PATTERN MATCHING ENGINE")
    print("=" * 42)
    print("1. Search Date")
    print("2. Search Phone Number")
    print("3. Search Hashtag")
    print("4. Search Mention")
    print("5. Search Prefix")
    print("6. Search Suffix")
    print("7. Search Word")
    print("8. Show text")
    print("0. Exit")


def main():
    text = load_text("text_data.txt")
    while True:
        menu()
        ch = input("Enter your choice: ").strip()
        if ch == "1":
            show("Dates", search_pattern(text, DATE_RE))
        elif ch == "2":
            show("Phone Numbers", search_pattern(text, PHONE_RE))
        elif ch == "3":
            show("Hashtags", search_pattern(text, HASHTAG_RE))
        elif ch == "4":
            show("Mentions", search_pattern(text, MENTION_RE))
        elif ch == "5":
            p = input("Enter prefix: ").strip()
            show(f"Words starting with '{p}'", search_prefix(text, p) if p else [])
        elif ch == "6":
            s = input("Enter suffix: ").strip()
            show(f"Words ending with '{s}'", search_suffix(text, s) if s else [])
        elif ch == "7":
            w = input("Enter word: ").strip()
            show(f"Lines containing the word '{w}'", search_word(text, w) if w else [])
        elif ch == "8":
            print("\n" + text)
        elif ch == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 0-8.")


if __name__ == "__main__":
    main()
