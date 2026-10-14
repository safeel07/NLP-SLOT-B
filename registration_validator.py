"""
Section 3 - University Registration Validation using Regular Expressions
Run in IDLE (F5). Keep 'students.csv' in the same folder as this file.

Validation rules
  Register No : 2 digits (year) + 3 uppercase letters (dept) + 4 digits   e.g. 23CSE1001
  Email       : name@university.edu.in (institutional domain)
  Course Code : 2-3 uppercase letters + 3 digits                          e.g. CS301
  Semester    : 1-8, optionally prefixed by 'Sem' / 'Semester'            e.g. 5, Sem 5
  Mobile      : 10 digits starting 6-9, optional +91 / 91 prefix
"""
import re
import csv
import os

RULES = {
    "reg_no": (re.compile(r"^\d{2}[A-Z]{3}\d{4}$"),
               "Register number must look like 23CSE1001"),
    "email": (re.compile(r"^[A-Za-z][A-Za-z0-9._-]*@university\.edu\.in$"),
              "Email must end with @university.edu.in"),
    "course_code": (re.compile(r"^[A-Z]{2,3}\d{3}$"),
                    "Course code must be 2-3 capital letters + 3 digits (e.g. CS301)"),
    "semester": (re.compile(r"^(?:Sem(?:ester)?\s*)?[1-8]$", re.I),
                 "Semester must be between 1 and 8"),
    "mobile": (re.compile(r"^(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}$"),
               "Mobile must be 10 digits starting with 6-9"),
}

LABELS = {"reg_no": "Register No", "email": "Email", "course_code": "Course Code",
          "semester": "Semester", "mobile": "Mobile"}


def validate_student(row):
    """Return (list of (field, ok, message), overall_status)."""
    results = []
    for field, (pattern, error) in RULES.items():
        value = row[field].strip()
        ok = bool(pattern.fullmatch(value))
        msg = "Valid" if ok else f"INVALID - {error}"
        results.append((field, ok, msg))
    return results, all(r[1] for r in results)


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.csv")
    with open(path, newline="", encoding="utf-8") as f:
        students = list(csv.DictReader(f))

    summary = []
    for s in students:
        results, status = validate_student(s)
        print("=" * 62)
        print(f"Student : {s['name']}")
        print("-" * 62)
        for field, ok, msg in results:
            mark = "[PASS]" if ok else "[FAIL]"
            print(f"  {mark} {LABELS[field]:<12}: {s[field]:<32} {msg}")
        print(f"  >> Registration Status: {'SUCCESSFUL' if status else 'REJECTED'}\n")
        summary.append((s["reg_no"], s["name"], status))

    print("=" * 62)
    print("            FINAL REGISTRATION STATUS REPORT")
    print("=" * 62)
    print(f"{'Reg No':<12}{'Name':<22}{'Status'}")
    print("-" * 62)
    for reg, name, ok in summary:
        print(f"{reg:<12}{name:<22}{'Registration Successful' if ok else 'Registration Failed'}")
    passed = sum(1 for _, _, ok in summary if ok)
    print("-" * 62)
    print(f"Total: {len(summary)} | Successful: {passed} | Failed: {len(summary) - passed}")


if __name__ == "__main__":
    main()
