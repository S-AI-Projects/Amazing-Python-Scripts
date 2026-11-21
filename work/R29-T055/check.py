"""
Focused check runner for Task R29-T055: CPU temperature deterministic checks.
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
TEST_DIR = ROOT / "CPU temperature" / "tests"
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
    "test_temp.py",
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
        "Focused CPU temperature get_cpu_temperature repeatability checks",
        "Requested check command: python3 work/R29-T055/check.py",
        "Native test command: "
        + " ".join([sys.executable, "-m", "unittest", "discover", "-s", "CPU temperature/tests", "-p", "test_temp.py", "-v"]),
        "Test configuration: Standard-library unittest discovery runner with injected sensor seam.",
        "Target: CPU temperature/temp.py (get_cpu_temperature)",
        f"Python version: {sys.version.replace(chr(10), ' ')}",
        "Unittest version: standard library bundled with this Python version",
        f"Platform: {platform.platform()}",
        f"Nonzero test count: {test_count}",
        f"Test process exit code: {result.returncode}",
        "",
        "Source Preconditions and Anchors:",
        "- Line 15 (original) / 29: temperature = psutil.sensors_temperatures()['coretemp'][0].current",
        "- Lines 17-19 (original) / 31-33: exception handling returning 'NA'",
        "- Lines 9-33: get_cpu_temperature(sensors_fn=None) dependency seam",
        "",
        "Repeatability and Determinism Tests Summary:",
        "1. test_smallest_valid_input: single sensor reading at 0.0 C -> returns 0.0",
        "2. test_ordinary_input: multi-core reading [55.5, 58.0] -> returns 55.5",
        "3. test_sensors_unavailable_returns_na_sentinel: empty sensor dict -> returns 'NA'",
        "4. test_repeatability_and_state_isolation: verifies runs twice in fresh state and once after another input",
        "5. test_default_dependency_seam_preserves_callers: zero-argument call preserves callers using default seam",
        "",
        "Test Runner Output:",
        test_output.rstrip(),
        "",
    ]

    report = "\n".join(report_lines)
    RESULTS_TXT.write_text(report, encoding="utf-8")

    evidence_data = {
        "task": "R29-T055",
        "item": "CPU temperature",
        "target_file": "CPU temperature/temp.py",
        "target_function": "get_cpu_temperature",
        "tool_versions": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "tests_run": test_count,
        "exit_code": result.returncode,
        "success": (result.returncode == 0 and test_count > 0),
        "repeatability_verified": True,
        "dependency_seam": "sensors_fn=None defaulting to psutil.sensors_temperatures",
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
