"""
Demonstration of Regular Expressions in Python (re module)
Matching and searching for patterns in text.
Run in IDLE (F5).
"""
import re

text = """Contact Alice at alice.smith@example.com or call 9876543210.
Bob's email is bob_99@mail.org and his phone is 8123456789.
Meeting scheduled on 12/09/2026 and follow-up on 25-12-2026.
Python is fun. python is powerful. PYTHON is popular."""


def heading(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# 1. re.match() - matches ONLY at the beginning of the string
heading("1. re.match()  - pattern at the START of the text")
m = re.match(r"Contact", text)
print("Pattern 'Contact' ->", m.group() if m else "No match")
m = re.match(r"Alice", text)
print("Pattern 'Alice'   ->", m.group() if m else "No match (not at the start)")

# 2. re.search() - finds the FIRST occurrence anywhere
heading("2. re.search() - first occurrence anywhere")
m = re.search(r"\d{10}", text)
if m:
    print("First 10-digit number:", m.group())
    print("Start index:", m.start(), "| End index:", m.end(), "| Span:", m.span())

# 3. re.fullmatch() - the WHOLE string must match
heading("3. re.fullmatch() - entire string must match")
for value in ["9876543210", "98765", "98765432101"]:
    ok = re.fullmatch(r"[6-9]\d{9}", value)
    print(f"{value:<14} -> {'Valid mobile' if ok else 'Invalid mobile'}")

# 4. re.findall() - list of ALL matches
heading("4. re.findall() - all matches as a list")
print("Emails :", re.findall(r"[\w.]+@[\w.]+\.\w+", text))
print("Phones :", re.findall(r"\b[6-9]\d{9}\b", text))
print("Dates  :", re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b", text))

# 5. re.finditer() - match objects with positions
heading("5. re.finditer() - matches with their positions")
for m in re.finditer(r"\b\d{10}\b", text):
    print(f"Found '{m.group()}' at index {m.start()}-{m.end()}")

# 6. Groups - capture parts of a match
heading("6. Groups - extracting parts of a match")
m = re.search(r"([\w.]+)@([\w.]+)\.(\w+)", text)
print("Full match :", m.group(0))
print("Username   :", m.group(1))
print("Domain     :", m.group(2))
print("Extension  :", m.group(3))

# Named groups on dates
for m in re.finditer(r"(?P<day>\d{1,2})[/-](?P<month>\d{1,2})[/-](?P<year>\d{4})", text):
    print(f"Date {m.group()} -> day={m.group('day')}, month={m.group('month')}, year={m.group('year')}")

# 7. Flags - case-insensitive and multi-line
heading("7. Flags - re.IGNORECASE and re.MULTILINE")
print("Case-sensitive   'python':", len(re.findall(r"python", text)))
print("Case-insensitive 'python':", len(re.findall(r"python", text, re.I)))
print("Lines starting with a capital letter (MULTILINE):",
      re.findall(r"^[A-Z]\w*", text, re.M))

# 8. re.sub() - search and replace
heading("8. re.sub() - replacing matched text")
masked = re.sub(r"\b(\d{6})(\d{4})\b", r"XXXXXX\2", text)
print(masked.splitlines()[0])
print(re.sub(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}", "<DATE>", text).splitlines()[2])

# 9. re.split() - splitting text using a pattern
heading("9. re.split() - splitting using a pattern")
print(re.split(r"[.\n]\s*", "one. two.three\nfour"))

# 10. re.compile() - reuse a pattern
heading("10. re.compile() - compiled pattern reused")
email_pat = re.compile(r"[A-Za-z][\w.]*@[A-Za-z]+\.(?:com|org|edu|net|in)")
for s in ["alice@example.com", "9bob@mail.org", "carl@site.xyz"]:
    print(f"{s:<22} -> {'Match' if email_pat.fullmatch(s) else 'No match'}")

# 11. Interactive search
heading("11. Search your own pattern")
while True:
    pattern = input("\nEnter a regex pattern (blank to quit): ")
    if not pattern:
        break
    try:
        results = [m.group() for m in re.finditer(pattern, text)]
        print(f"{len(results)} match(es):", results)
    except re.error as e:
        print("Invalid regular expression:", e)
print("\nDone.")
