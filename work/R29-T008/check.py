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
    "Health_Log_Book/tests",
    "-p",
    "test_getdate.py",
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
            "Focused Health Log getdate branch checks",
            "Requested check command: python3 work/R29-T008/check.py",
            "Native test command: "
            + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
            "No root test configuration exists; the focused tests use standard-library unittest.",
            "Source facts recorded before edits: getdate() takes no arguments "
            "and directly returns datetime.datetime.now() at main.py line 12. "
            "There is no failure, sentinel, or missing-result branch in this "
            "implementation. The smallest valid return value is datetime.min. "
            "Tkinter widgets, database connection/setup, GUI output, and clock "
            "state are mocked; import does not contact external services.",
            "The supplied tv['columns'] fixture belongs to the separate show-log "
            "GUI path (main.py lines 66 and 108), not getdate.",
            f"Python version: {sys.version.replace(chr(10), ' ')}",
            "Unittest version: standard library bundled with this Python version",
            f"Platform: {platform.platform()}",
            f"Nonzero test count: {test_count}",
            f"Test process exit code: {result.returncode}",
            "",
            "Literal fixture inputs, expected values, actual values, and test output:",
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
