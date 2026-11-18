import platform
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
RESULTS = Path(__file__).resolve().parent / "results.txt"
TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    "Football-Player-Club-Info/tests",
    "-p",
    "test_my_scraper.py",
    "-v",
]


def main():
    result = subprocess.run(
        TEST_COMMAND,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    test_output = result.stdout + result.stderr
    test_count_match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(test_count_match.group(1)) if test_count_match else 0
    report = "\n".join(
        [
            "Focused Football-Player-Club-Info myScraper reference checks",
            "Requested check command: python3 work/R29-T003/check.py",
            "Native test command: "
            + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
            "No repository-wide pytest/unittest configuration was found; "
            "the focused tests use standard-library unittest.",
            "Source contract: main.py lines 11-18 take a player name, fetch "
            "the corresponding English Wikipedia page, parse its text, and "
            "store the player without mutating that input. README lines 25-26 "
            "state that club-career sections are retrieved and printed. "
            "main.py lines 20-41 print the selected section titles in order; "
            "execute() returns None.",
            "Baseline minimal counterexample before the filter fix: player "
            "'Fixture Player'; sections=[('Overview', [('Biography', [])])]; "
            "expected output=''; actual output='Biography\\n'. This is one "
            "non-club root with one child and establishes the smallest "
            "mismatch. The ordinary baseline fixture also printed its "
            "non-club 'Early life' child before the club-career titles.",
            "Independent oracle: flatten only root sections whose title "
            "contains 'Club career', then append child and grandchild titles "
            "in fixture order. It does not call myScraper. Twenty small "
            "deterministic section trees are compared against this reference.",
            "External Wikipedia/API and parser dependencies are stubbed; "
            "no network request or live credentials are used. Each comparison "
            "uses fresh scraper and section objects and verifies input "
            "preservation.",
            f"Python version: {sys.version.replace(chr(10), ' ')}",
            "Unittest version: standard library bundled with this Python version",
            f"Platform: {platform.platform()}",
            f"Nonzero test count: {test_count}",
            "Independent small section-tree inputs compared: 20",
            f"Test process exit code: {result.returncode}",
            "",
            "Literal fixtures, expected versus actual outputs, and test output:",
            test_output.rstrip(),
            "",
        ]
    )
    RESULTS.write_text(report, encoding="utf-8")
    sys.stdout.write(test_output)
    sys.stdout.write(f"\nSaved evidence to {RESULTS.relative_to(ROOT)}.\n")
    if test_count == 0:
        sys.stderr.write("The focused unittest command did not run any tests.\n")
        return 1
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
