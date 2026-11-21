#!/usr/bin/env python3
"""Automated check runner for R29-T058.

Task: Cover the failure behavior of start_game (Color_guess.py) [Color Guess-GUI]
Target: Color Guess-GUI/Color_guess.py
"""

import io
import json
import os
import platform
import sys
import unittest
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent
REPO_ROOT = WORK_DIR.parent.parent
MODULE_DIR = REPO_ROOT / "Color Guess-GUI"

# Add paths for imports
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import module and tests
import Color_guess
from tests.test_color_guess import TestColorGuessFailureBehavior


def run_checks():
    """Run focused unit tests and record evidence."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestColorGuessFailureBehavior)

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    output = stream.getvalue()
    print(output)

    # Prepare evidence dictionary
    evidence = {
        "task": "R29-T058",
        "item": "Color Guess-GUI",
        "target_file": "Color Guess-GUI/Color_guess.py",
        "target_function": "start_game",
        "data_anchors": {
            "source_lines_colors_name": "Lines 4-5: colors_name = ['Red', 'White', 'Yellow', 'Pink', 'Blue', 'Black', 'Brown', 'Purple', 'Green', 'Cyan']",
            "source_lines_initial_state": "Lines 6-7: score = 0, time_left = 60",
            "source_line_active_branch": "Line 11: if time_left == 60: countdown()",
            "source_line_absent_result_branch": "Line 19: if (time_left > 0): in change_color()",
            "source_line_rejection_branch": "Line 21: if e.get().lower() == colors_name[1].lower():",
            "source_line_countdown_branch": "Line 32: if time_left > 0: in countdown()"
        },
        "fixtures": {
            "smallest_valid_input_absent_result": {
                "play": None,
                "time_left": 0,
                "score": 0,
                "expected_return": None,
                "expected_score_after": 0,
                "expected_time_left_after": 0,
                "expected_e_text_after": "White"
            },
            "ordinary_valid_input_active": {
                "play": None,
                "time_left": 60,
                "score": 0,
                "entry_input": "White",
                "expected_return": None,
                "expected_score_after": 1,
                "expected_time_left_after": 59,
                "expected_e_text_after": ""
            }
        },
        "python_version": sys.version,
        "platform": platform.platform(),
        "tests_run": result.testsRun,
        "errors": len(result.errors),
        "failures": len(result.failures),
        "successful": result.wasSuccessful()
    }

    results_json_path = WORK_DIR / "results.json"
    results_txt_path = WORK_DIR / "results.txt"

    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)

    with open(results_txt_path, "w", encoding="utf-8") as f:
        f.write(f"Task: R29-T058 Check Results\n")
        f.write(f"Target: Color Guess-GUI/Color_guess.py\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {platform.platform()}\n")
        f.write(f"Tests run: {result.testsRun}\n")
        f.write(f"Failures: {len(result.failures)}\n")
        f.write(f"Errors: {len(result.errors)}\n")
        f.write(f"Status: {'PASSED' if result.wasSuccessful() else 'FAILED'}\n\n")
        f.write("Output:\n")
        f.write(output)

    if not result.wasSuccessful():
        print(f"FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
        sys.exit(1)

    print(f"SUCCESS: All {result.testsRun} checks passed.")
    sys.exit(0)


if __name__ == '__main__':
    run_checks()
