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
    "AWS Management Scripts/AWS testing Script/tests",
    "-p",
    "test_aws_handler.py",
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
            "Focused AWS EC2 launch-parameter refactor checks",
            "Requested check command: python3 work/R29-T006/check.py",
            "Native test command: "
            + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
            "Test configuration: no root Python test configuration exists; "
            "the project has no test runner for this item, so standard-library "
            "unittest is used.",
            "The EC2 SDK client is a fake that records run_instances calls; "
            "no AWS SDK, credentials, or live network access are used.",
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
    with RESULTS.open("a", encoding="utf-8") as evidence:
        if evidence.tell():
            evidence.write("\n---\n")
        evidence.write(report)
    sys.stdout.write(test_output)
    sys.stdout.write(f"\nSaved evidence to {RESULTS.relative_to(ROOT)}.\n")
    if test_count == 0:
        sys.stderr.write("The focused unittest command did not run any tests.\n")
        return 1
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
