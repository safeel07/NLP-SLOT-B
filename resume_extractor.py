"""
Section 1 - Resume Information Extraction using Regular Expressions
Run in IDLE (F5). Keep 'resumes.txt' in the same folder as this file.
"""
import re
import os

# ---------- Compiled regular expressions ----------
NAME_RE   = re.compile(r"^\s*Name\s*[:\-]\s*([A-Za-z][A-Za-z .']+?)\s*$", re.I | re.M)
EMAIL_RE  = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
MOBILE_RE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")
SKILL_RE  = re.compile(r"\b(Python|Java|SQL|Machine\s+Learning|NLP)\b", re.I)
EXP_RE    = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\b", re.I)

SKILL_NAMES = {"python": "Python", "java": "Java", "sql": "SQL",
               "nlp": "NLP", "machine learning": "Machine Learning"}

MIN_EXPERIENCE = 2
REQUIRED_SKILL = "Python"


def load_resumes(filename):
    """Read the file and split it into individual resumes."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [r.strip() for r in re.split(r"^=+\s*$", text, flags=re.M) if r.strip()]


def extract_name(resume):
    m = NAME_RE.search(resume)
    return m.group(1) if m else "Not found"


def extract_emails(resume):
    return EMAIL_RE.findall(resume)


def extract_mobiles(resume):
    return [re.sub(r"[\s-]", "", m) for m in MOBILE_RE.findall(resume)]


def extract_skills(resume):
    found = []
    for s in SKILL_RE.findall(resume):
        key = re.sub(r"\s+", " ", s.lower())
        name = SKILL_NAMES[key]
        if name not in found:
            found.append(name)
    return found


def extract_experience(resume):
    years = [float(y) for y in EXP_RE.findall(resume)]
    return max(years) if years else 0.0


def build_profile(resume):
    return {
        "name":   extract_name(resume),
        "emails": extract_emails(resume),
        "mobiles": extract_mobiles(resume),
        "skills": extract_skills(resume),
        "experience": extract_experience(resume),
    }


def print_summary(p, no):
    print(f"Candidate #{no}")
    print("-" * 50)
    print(f"  Name       : {p['name']}")
    print(f"  Email      : {', '.join(p['emails']) or 'Not found'}")
    print(f"  Mobile     : {', '.join(p['mobiles']) or 'Not found'}")
    print(f"  Skills     : {', '.join(p['skills']) or 'None detected'}")
    print(f"  Experience : {p['experience']:g} years")
    print()


def is_eligible(p):
    return p["experience"] >= MIN_EXPERIENCE and REQUIRED_SKILL in p["skills"]


def main():
    resumes = load_resumes("resumes.txt")
    profiles = [build_profile(r) for r in resumes]

    print("=" * 50)
    print("   STRUCTURED CANDIDATE PROFILE SUMMARY")
    print("=" * 50)
    for i, p in enumerate(profiles, 1):
        print_summary(p, i)

    print("=" * 50)
    print(f"  SHORTLISTED (>= {MIN_EXPERIENCE} yrs experience AND {REQUIRED_SKILL} skill)")
    print("=" * 50)
    shortlisted = [p for p in profiles if is_eligible(p)]
    if shortlisted:
        print(f"{'Name':<18}{'Experience':<13}{'Email':<32}{'Mobile'}")
        for p in shortlisted:
            print(f"{p['name']:<18}{str(p['experience'])+' yrs':<13}"
                  f"{(p['emails'] or ['-'])[0]:<32}{(p['mobiles'] or ['-'])[0]}")
    else:
        print("No candidate satisfies the criteria.")
    print(f"\nTotal resumes: {len(profiles)} | Shortlisted: {len(shortlisted)}")


if __name__ == "__main__":
    main()
