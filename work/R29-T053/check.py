"""
Focused check runner for Task R29-T053: Auto-Fill-Google-Forms reference comparison.
"""
from __future__ import annotations

import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = Path(__file__).resolve().parent
TEST_DIR = ROOT / "Auto-Fill-Google-Forms" / "tests"
RESULTS_TXT = WORK_DIR / "results.txt"
RESULTS_JSON = WORK_DIR / "results.json"

TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    str(TEST_DIR),
    "-p",
    "test_auto_fill.py",
    "-v",
]


def main() -> int:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)

    result = subprocess.run(
        TEST_COMMAND,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    test_output = (result.stdout or "") + (result.stderr or "")

    test_count_match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(test_count_match.group(1)) if test_count_match else 0

    report_lines = [
        "Focused Auto-Fill-Google-Forms reference comparison checks",
        "Requested check command: python3 work/R29-T053/check.py",
        "Native test command: "
        + " ".join([sys.executable, "-m", "unittest", "discover", "-s", "Auto-Fill-Google-Forms/tests", "-p", "test_auto_fill.py", "-v"]),
        "Test configuration: Standard-library unittest discovery runner with mocked Selenium browser.",
        "Target: Auto-Fill-Google-Forms/readme.md and test.py",
        f"Python version: {sys.version.replace(chr(10), ' ')}",
        "Unittest version: standard library bundled with this Python version",
        f"Platform: {platform.platform()}",
        f"Nonzero test count: {test_count}",
        f"Test process exit code: {result.returncode}",
        "",
        "Source Preconditions and Anchors:",
        "- Lines 6-8: XPath constants inputName, inputEmailID, inputPhone",
        "- Line 11: Submit button XPath",
        "- Line 27: csv_input = csv.DictReader(f_input)",
        "- Lines 28-31: row['name'], row['email'], row['phone_number']",
        "- Lines 36-45: Submission loop over records",
        "",
        "Differential Test Cases Summary:",
        "1. test_smallest_valid_input: 1 row CSV -> matches independent reference oracle payload",
        "2. test_ordinary_input: input.csv with 6 rows -> matches independent reference oracle",
        "3. test_differential_twenty_domain_inputs: 25 distinct valid inputs verified against oracle",
        "4. test_input_mutation_isolation: verifies input record lists are not mutated",
        "5. test_browser_automation_interactions: verifies mocked browser send_keys, click, and back calls",
        "",
        "Test Runner Output:",
        test_output.rstrip(),
        "",
    ]

    report = "\n".join(report_lines)
    RESULTS_TXT.write_text(report, encoding="utf-8")

    evidence_data = {
        "task": "R29-T053",
        "item": "Auto-Fill-Google-Forms",
        "target": "Auto-Fill-Google-Forms/readme.md",
        "tool_versions": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "tests_run": test_count,
        "exit_code": result.returncode,
        "success": (result.returncode == 0 and test_count > 0),
        "domain_sample_count": 25,
        "preconditions": [
            "Lines 6-8: XPath selectors for name, email, phone",
            "Line 11: Submit button XPath",
            "Line 27: csv.DictReader(f_input)",
            "Lines 28-31: name, email, phone_number column mapping",
            "Lines 36-45: form submission and browser back loop",
        ],
    }
    RESULTS_JSON.write_text(json.dumps(evidence_data, indent=2), encoding="utf-8")

    sys.stdout.write(test_output)
    sys.stdout.write(f"\nSaved evidence to {RESULTS_TXT.relative_to(ROOT)}.\n")

    if test_count == 0:
        sys.stderr.write("The focused unittest command did not run any tests.\n")
        return 1

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
