#!/usr/bin/env python3
"""
Test runner for R29-T035: Make verification repeatable for resize_image (app.py) [Image to ASCII Art].
Executes controlled tests, verifies repeatability and input non-mutation,
and records inputs, outputs, and tool versions under work/R29-T035/.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T035")
ASCII_DIR = os.path.join(ROOT_DIR, "Image to ASCII Art")

if ASCII_DIR not in sys.path:
    sys.path.insert(0, ASCII_DIR)

import app
import test_app
from test_app import MockImage


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T035",
        "target": "Image to ASCII Art/app.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Smallest valid input
    img_min = MockImage((1, 1))
    res_min = app.resize_image(img_min, new_width=1)
    test_1 = {
        "name": "smallest_valid_input_resize_image",
        "source_preconditions": "Image to ASCII Art/app.py lines 24-27",
        "input": {"original_size": [1, 1], "new_width": 1},
        "expected": [1, 1],
        "actual": list(res_min.size),
        "passed": res_min.size == (1, 1) and img_min.size == (1, 1)
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary input
    img_ord = MockImage((800, 600))
    res_ord = app.resize_image(img_ord, new_width=100)
    test_2 = {
        "name": "ordinary_input_resize_image",
        "source_preconditions": "Image to ASCII Art/app.py lines 24-27",
        "input": {"original_size": [800, 600], "new_width": 100},
        "expected": [100, 75],
        "actual": list(res_ord.size),
        "passed": res_ord.size == (100, 75) and img_ord.size == (800, 600)
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}", file=sys.stderr)
        sys.exit(1)

    # 3. Repeatability check across 5 iterations
    img_rep = MockImage((400, 200))
    runs = [app.resize_image(img_rep, 50).size for _ in range(5)]
    all_repeatable = all(s == (50, 25) for s in runs) and img_rep.size == (400, 200)
    test_3 = {
        "name": "repeatable_idempotency_check",
        "source_preconditions": "Image to ASCII Art/app.py lines 24-27",
        "runs_count": 5,
        "expected_each": [50, 25],
        "passed": all_repeatable
    }
    evidence["tests"].append(test_3)
    if not all_repeatable:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_app)
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
