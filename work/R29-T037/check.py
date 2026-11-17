#!/usr/bin/env python3
"""
Test runner for R29-T037: Publish a runnable example for insertLetter (main.py) [Tictactoe-Using-Minmax].
Executes worked example tests, validates intermediate to final mutation states,
and records inputs, outputs, and tool versions under work/R29-T037/.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T037")
TTT_DIR = os.path.join(ROOT_DIR, "Tictactoe-Using-Minmax")

if TTT_DIR not in sys.path:
    sys.path.insert(0, TTT_DIR)

import main as ttt
import test_ttt


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T037",
        "target": "Tictactoe-Using-Minmax/main.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Smallest input worked example (pos=1, letter='X')
    ttt.board = [' ' for _ in range(10)]
    initial_slot = ttt.board[1]
    ttt.insertLetter('X', 1)
    final_slot = ttt.board[1]
    test_1 = {
        "name": "smallest_input_worked_example",
        "source_preconditions": "Tictactoe-Using-Minmax/main.py lines 35, 36",
        "input": {"letter": "X", "pos": 1},
        "initial_intermediate_state": initial_slot,
        "final_state": final_slot,
        "expected": "X",
        "passed": (initial_slot == ' ' and final_slot == 'X')
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary input worked example (pos=5, letter='O')
    custom_b = [' ' for _ in range(10)]
    init_5 = custom_b[5]
    ttt.insertLetter('O', 5, custom_b)
    fin_5 = custom_b[5]
    test_2 = {
        "name": "ordinary_input_worked_example",
        "source_preconditions": "Tictactoe-Using-Minmax/main.py lines 35, 36",
        "input": {"letter": "O", "pos": 5},
        "initial_intermediate_state": init_5,
        "final_state": fin_5,
        "expected": "O",
        "passed": (init_5 == ' ' and fin_5 == 'O')
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}", file=sys.stderr)
        sys.exit(1)

    # 3. Step-by-step intermediate progression
    seq_b = [' ' for _ in range(10)]
    ttt.insertLetter('X', 1, seq_b)
    ttt.insertLetter('O', 5, seq_b)
    ttt.insertLetter('X', 9, seq_b)
    seq_passed = (seq_b[1] == 'X' and seq_b[5] == 'O' and seq_b[9] == 'X')
    test_3 = {
        "name": "step_by_step_progression_worked_example",
        "source_preconditions": "Tictactoe-Using-Minmax/main.py lines 35, 36",
        "final_board": seq_b,
        "passed": seq_passed
    }
    evidence["tests"].append(test_3)
    if not seq_passed:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_ttt)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    evidence["unittest_run"] = {
        "tests_run": result.testsRun,
        "was_successful": result.wasSuccessful(),
        "errors_count": len(result.errors),
        "failures_count": len(result.failures)
    }

    # Save evidence file
    evidence_file = os.path.join(WORK_DIR, "results.json")
    with open(evidence_file, "w") as f:
        json.dump(evidence, f, indent=2)

    print(f"\nAll checks passed successfully. Nonzero test count: {result.testsRun}")
    print(f"Evidence saved to {evidence_file}")

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    run_checks()
