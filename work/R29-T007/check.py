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
    "Amazon-Price-Tracker/tests",
    "-p",
    "test_message_sending.py",
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
            "Focused message_sending executable documentation checks",
            "Requested check command: python3 work/R29-T007/check.py",
            "Native test command: "
            + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
            "Test configuration: no root Python test configuration exists; "
            "the project has no test runner for this item, so standard-library "
            "unittest is used.",
            "Source facts recorded before edits: message_sending(phone_number, "
            "title) reads the current datetime, builds an alert string, calls "
            "pywhatkit.sendwhatmsg with phone, message, hour, and minute + 1, "
            "returns None, and does not mutate its string arguments. External "
            "dependencies are datetime and pywhatkit; module import also prompts "
            "for input, makes an HTTP request, and starts a polling loop, all "
            "mocked/stopped by the focused test.",
            "Baseline against the original implementation: the smallest-title "
            "and ordinary fixtures passed (2 tests) with exact expected and "
            "actual call arguments.",
            "The separate request-header fixture is established at "
            "amazonprice.py line 20; message_sending does not read or mutate it.",
            "Manual ordinary trace: now=2024-01-02 14:08; title="
            "'Stainless Steel Bottle'; message='Price of Stainless Steel Bottle "
            "is fallen below the threshold amount. Click on the link below to "
            "buy the product!!!\\\\n\\\\n'; schedule=(14, 9).",
            "requests, BeautifulSoup, pywhatkit, input, and sleep are mocked; "
            "no network, WhatsApp, or long-running tracker loop is used.",
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
