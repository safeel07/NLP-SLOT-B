"""
Section 2 - Product Search System using Regular Expressions
Run in IDLE (F5). Keep 'products.txt' in the same folder as this file.
"""
import re
import os


def load_products(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def build_pattern(keyword, mode):
    """Return a regex pattern string for the chosen search mode."""
    k = re.escape(keyword)
    if mode == "exact":
        return rf"\b{k}\b"          # whole word / whole phrase
    if mode == "prefix":
        return rf"\b{k}\w*"         # words starting with keyword
    if mode == "suffix":
        return rf"\w*{k}\b"         # words ending with keyword
    if mode == "partial":
        return k                    # keyword anywhere
    raise ValueError("Unknown mode")


def search(products, keyword, mode="exact", ignore_case=True):
    flags = re.I if ignore_case else 0
    pattern = re.compile(build_pattern(keyword, mode), flags)
    return [p for p in products if pattern.search(p)]


def run_and_report(products, tests):
    report = []
    for keyword, mode, ic in tests:
        results = search(products, keyword, mode, ic)
        case_txt = "Case-insensitive" if ic else "Case-sensitive"
        print("=" * 60)
        print(f"Search : '{keyword}' | Type: {mode.upper()} | {case_txt}")
        print("-" * 60)
        if results:
            for r in results:
                print("   *", r)
        else:
            print("   No matching products found.")
        print(f"Matches: {len(results)}\n")
        report.append((keyword, mode, case_txt, len(results)))

    print("=" * 60)
    print("                 SEARCH SUMMARY REPORT")
    print("=" * 60)
    print(f"{'No':<4}{'Keyword':<14}{'Search Type':<13}{'Case Mode':<18}{'Matches'}")
    print("-" * 60)
    for i, (k, m, c, n) in enumerate(report, 1):
        print(f"{i:<4}{k:<14}{m:<13}{c:<18}{n}")
    print("-" * 60)
    print(f"Total matching products across all searches: {sum(r[3] for r in report)}")


def interactive(products):
    print("\n--- Interactive Search (press Enter on keyword to quit) ---")
    while True:
        kw = input("\nEnter keyword: ").strip()
        if not kw:
            break
        mode = input("Mode [exact/prefix/suffix/partial]: ").strip().lower() or "partial"
        ic = input("Ignore case? [y/n]: ").strip().lower() != "n"
        try:
            res = search(products, kw, mode, ic)
        except ValueError:
            print("Invalid mode.")
            continue
        for r in res:
            print("   *", r)
        print(f"Total matching products: {len(res)}")


def main():
    products = load_products("products.txt")
    print(f"Loaded {len(products)} products.\n")

    tests = [
        ("Laptop",   "exact",   True),    # exact keyword
        ("Apple",    "prefix",  True),    # prefix based
        ("Blue",     "prefix",  True),    # prefix based (Bluetooth)
        ("phones",   "suffix",  True),    # suffix based (Headphones)
        ("board",    "suffix",  True),    # suffix based (Keyboard)
        ("watch",    "partial", True),    # partial keyword
        ("wire",     "partial", True),    # partial keyword (Wireless)
        ("smart",    "exact",   True),    # case-insensitive
        ("smart",    "exact",   False),   # case-sensitive -> compare result
        ("Running",  "exact",   False),
    ]
    run_and_report(products, tests)
    interactive(products)


if __name__ == "__main__":
    main()
