#!/usr/bin/env python3
"""Automated check runner for R29-T056.

Task: Simplify one responsibility in display_board (TicTacToe.py) [AI TicTacToe]
Target: AI TicTacToe/TicTacToe.py
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
MODULE_DIR = REPO_ROOT / "AI TicTacToe"

# Add paths for imports
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import module and tests
import TicTacToe
from tests.test_tic_tac_toe import TestDisplayBoard


def run_checks():
    """Run focused unit tests and record evidence."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDisplayBoard)

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    output = stream.getvalue()
    print(output)

    # Prepare evidence dictionary
    evidence = {
        "task": "R29-T056",
        "item": "AI TicTacToe",
        "target_file": "AI TicTacToe/TicTacToe.py",
        "function_refactored": "display_board",
        "extracted_helper": "format_row",
        "data_anchors": {
            "source_line_board_init": "Line 63: the_board = [' '] * 10",
            "source_lines_display_board": "Lines 4-18: format_row and display_board",
            "source_lines_winning_combinations": "Lines 35-39: winning_combinations triplets [1, 2, 3], [4, 5, 6], [7, 8, 9]"
        },
        "fixtures": {
            "smallest_valid_input": {
                "input": [" "] * 10,
                "expected_output": (
                    "-------------\n"
                    "|   |   |   |\n"
                    "-------------\n"
                    "|   |   |   |\n"
                    "-------------\n"
                    "|   |   |   |\n"
                    "-------------\n"
                )
            },
            "ordinary_input": {
                "input": [' ', 'X', 'O', 'X', ' ', 'X', 'O', 'O', ' ', 'X'],
                "expected_output": (
                    "-------------\n"
                    "| O |   | X |\n"
                    "-------------\n"
                    "|   | X | O |\n"
                    "-------------\n"
                    "| X | O | X |\n"
                    "-------------\n"
                )
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
        f.write(f"Task: R29-T056 Check Results\n")
        f.write(f"Target: AI TicTacToe/TicTacToe.py\n")
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
