"""
Focused check runner for Task R29-T051: Codechef Scrapper get_problems contract.
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
TEST_DIR = ROOT / "Codechef Scrapper" / "tests"
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
    "test_codechef.py",
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
        "Focused Codechef Scrapper get_problems contract and regression checks",
        "Requested check command: python3 work/R29-T051/check.py",
        "Native test command: "
        + " ".join([sys.executable, "-m", "unittest", "discover", "-s", "Codechef Scrapper/tests", "-p", "test_codechef.py", "-v"]),
        "Test configuration: Standard-library unittest discovery runner with mocked Selenium webdriver and FPDF.",
        "Target: Codechef Scrapper/codechef.py (get_problems)",
        f"Python version: {sys.version.replace(chr(10), ' ')}",
        "Unittest version: standard library bundled with this Python version",
        f"Platform: {platform.platform()}",
        f"Nonzero test count: {test_count}",
        f"Test process exit code: {result.returncode}",
        "",
        "Source Precondition and Fixture Anchors:",
        "- Line 18: baseurl = 'https://www.codechef.com/problems'",
        "- Line 19: wait = WebDriverWait(driver, 15)",
        "- Lines 22-23: problem_difficulty = {'Beginner': 'school', 'Easy': 'easy', 'Medium': 'medium', 'Hard': 'hard', 'Challenge': 'challenge'}",
        "- Line 31 (original) / 53: problem_info = {}",
        "- Lines 63-71 (original 41-48): table scraping loop, key assignment problem_info[problem_name] = problem_url",
        "",
        "Test Cases Summary:",
        "1. test_smallest_valid_input: category='school', no_of_problems=1 -> expected {'ATM': 'https://www.codechef.com/problems/HS08TEST'}",
        "2. test_ordinary_input: category='easy', no_of_problems=2 -> expected 2 problem items mapping names to links",
        "3. test_repeated_value_domain_boundary: category='medium', no_of_problems=2 with duplicate names -> key deduplication preserves latest URL",
        "4. test_zero_problems_boundary: category='school', no_of_problems=0 -> returns empty dict {} matching anchor problem_info = {}",
        "5. test_observable_mutation_and_state_isolation: verifies problem_difficulty unmutated and return dict is caller-isolated",
        "",
        "Test Runner Output:",
        test_output.rstrip(),
        "",
    ]

    report = "\n".join(report_lines)
    RESULTS_TXT.write_text(report, encoding="utf-8")

    evidence_data = {
        "task": "R29-T051",
        "item": "Codechef Scrapper",
        "target_file": "Codechef Scrapper/codechef.py",
        "target_function": "get_problems",
        "tool_versions": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "tests_run": test_count,
        "exit_code": result.returncode,
        "success": (result.returncode == 0 and test_count > 0),
        "preconditions": [
            "Line 18: baseurl = 'https://www.codechef.com/problems'",
            "Line 19: wait = WebDriverWait(driver, 15)",
            "Lines 22-23: problem_difficulty = {'Beginner': 'school', 'Easy': 'easy', 'Medium': 'medium', 'Hard': 'hard', 'Challenge': 'challenge'}",
            "Line 31 (original) / 53: problem_info = {}",
            "Lines 63-71 (original 41-48): problem_info[problem_name] = problem_url",
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
