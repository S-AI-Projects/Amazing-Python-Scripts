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
    "AI Chat Bot/tests",
    "-p",
    "test_animate.py",
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
            "Focused AI Chat Bot animate deterministic checks",
            "Requested check command: python3 work/R29-T005/check.py",
            "Native test command: "
            + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
            "No repository-wide pytest/unittest configuration was found; "
            "the focused tests use standard-library unittest.",
            "Source facts: animate() at main.py lines 22-33 has no parameters "
            "or return value. It reads the shared done flag at line 25, emits "
            "spinner frames from the cycle at lines 24 and 27, sleeps at line "
            "29, and clears the line at line 32. Its observable dependencies "
            "are the done flag, stdout, and time.sleep. The test controls "
            "done and mocks sleep/stdout; network and GUI are not invoked. "
            "The module initializes done to False at line 19.",
            "The supplied headers and payload fixture belongs to ask() at "
            "main.py lines 36-39, not animate().",
            "Literal invocations: animate() with one controlled frame "
            "(smallest run) and animate() with three controlled frames "
            "(ordinary run). Expected output strings are asserted exactly; "
            "the one-frame input is repeated twice and then repeated after "
            "the ordinary run to check isolation.",
            "The focused tests mock imports of requests and pyfiglet because "
            "the declared packages are not installed; no external API request "
            "or interactive GUI/user input is used.",
            f"Python version: {sys.version.replace(chr(10), ' ')}",
            "Unittest version: standard library bundled with this Python version",
            f"Platform: {platform.platform()}",
            f"Nonzero test count: {test_count}",
            f"Test process exit code: {result.returncode}",
            "",
            "Literal inputs, expected values, actual values, and test output:",
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
