"""
Section 1 - User Registration Credential Validation (Regular Expressions)
Run in IDLE (F5). Keep 'users.csv' in the same folder.
"""
import re
import csv
import os

EMAIL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._]*@[A-Za-z]+\.(?:com|org|edu|net|in)$")
MOBILE_RE = re.compile(r"^[6-9]\d{9}$")

# Individual password rules (used to explain why a password is weak)
PASSWORD_RULES = [
    (re.compile(r".{8,}"),        "minimum 8 characters"),
    (re.compile(r"[A-Z]"),        "an uppercase letter"),
    (re.compile(r"[a-z]"),        "a lowercase letter"),
    (re.compile(r"\d"),           "a digit"),
    (re.compile(r"[@#$%&!]"),     "a special character (@ # $ % & !)"),
]
# Complete password policy in a single expression using look-aheads
PASSWORD_RE = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&!]).{8,}$")


def validate_email(email):
    return bool(EMAIL_RE.fullmatch(email))


def validate_password(pwd):
    return bool(PASSWORD_RE.fullmatch(pwd))


def password_missing(pwd):
    return [msg for rule, msg in PASSWORD_RULES if not rule.search(pwd)]


def validate_mobile(mobile):
    return bool(MOBILE_RE.fullmatch(mobile))


def check_user(email, pwd, mobile, no=None):
    title = f"User #{no}" if no else "User"
    print("=" * 60)
    print(title)
    print("-" * 60)
    print(f"  Email    : {email}")
    print(f"     -> {'Valid Email' if validate_email(email) else 'Invalid Email'}")

    print(f"  Password : {pwd}")
    if validate_password(pwd):
        print("     -> Strong Password")
    else:
        print("     -> Weak Password (missing: " + ", ".join(password_missing(pwd)) + ")")

    print(f"  Mobile   : {mobile}")
    print(f"     -> {'Valid Mobile Number' if validate_mobile(mobile) else 'Invalid Mobile Number'}")
    ok = validate_email(email) and validate_password(pwd) and validate_mobile(mobile)
    print(f"  >> Account creation: {'ALLOWED' if ok else 'BLOCKED'}\n")
    return ok


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.csv")
    with open(path, newline="", encoding="utf-8") as f:
        users = list(csv.DictReader(f))

    passed = 0
    for i, u in enumerate(users, 1):
        if check_user(u["email"].strip(), u["password"].strip(), u["mobile"].strip(), i):
            passed += 1
    print("=" * 60)
    print(f"Total users: {len(users)} | Allowed: {passed} | Blocked: {len(users) - passed}")

    # ---- optional interactive check ----
    print("\n--- Try your own credentials (press Enter on email to quit) ---")
    while True:
        e = input("\nEmail    : ").strip()
        if not e:
            break
        p = input("Password : ").strip()
        m = input("Mobile   : ").strip()
        check_user(e, p, m)


if __name__ == "__main__":
    main()
