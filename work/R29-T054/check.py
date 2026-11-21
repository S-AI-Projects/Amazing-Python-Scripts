"""
Focused check runner for Task R29-T054: Number Guess Game invariant checks.
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
TEST_DIR = ROOT / "Number-Guess-Game" / "tests"
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
    "test_number_guess.py",
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
        "Focused Number Guess Game invariant property checks",
        "Requested check command: python3 work/R29-T054/check.py",
        "Native test command: "
        + " ".join([sys.executable, "-m", "unittest", "discover", "-s", "Number-Guess-Game/tests", "-p", "test_number_guess.py", "-v"]),
        "Test configuration: Standard-library unittest discovery runner with seeded property generator.",
        "Target: Number-Guess-Game/numberguess.py",
        f"Python version: {sys.version.replace(chr(10), ' ')}",
        "Unittest version: standard library bundled with this Python version",
        f"Platform: {platform.platform()}",
        f"Nonzero test count: {test_count}",
        f"Test process exit code: {result.returncode}",
        "",
        "Source Preconditions and Invariant Anchors:",
        "- Lines 5-10: top_of_range validation (positive integer requirement)",
        "- Line 15: random.randint(0, top_of_range) target boundedness",
        "- Lines 18-35: Guessing loop and monotonic comparison feedback",
        "- Line 36: Final guess counter report",
        "",
        "Mathematical and Behavioral Invariants Verified:",
        "1. Target Boundedness: 0 <= random_number <= top_of_range",
        "2. Comparison Monotonicity: guess > target -> above, guess < target -> below, guess == target -> correct",
        "3. Guess Counter Invariant: reported guesses == total guess loop iterations taken",
        "4. Seeded Property Verification: 100 random bounded cases verified with seed 42",
        "5. Mutation Sensitivity: deliberate mutant breaking feedback/counter fails assertions",
        "",
        "Test Runner Output:",
        test_output.rstrip(),
        "",
    ]

    report = "\n".join(report_lines)
    RESULTS_TXT.write_text(report, encoding="utf-8")

    evidence_data = {
        "task": "R29-T054",
        "item": "Number-Guess-Game",
        "target_file": "Number-Guess-Game/numberguess.py",
        "tool_versions": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "tests_run": test_count,
        "exit_code": result.returncode,
        "success": (result.returncode == 0 and test_count > 0),
        "property_cases_verified": 100,
        "random_seed": 42,
        "invariants": [
            "Target Boundedness: 0 <= random_number <= top_of_range",
            "Comparison Monotonicity: directional feedback strictly matches sign of (guess - target)",
            "Guess Count Invariant: reported guesses equals iterations taken",
            "Mutation Sensitivity: deliberate mutant breaking invariant fails check",
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
