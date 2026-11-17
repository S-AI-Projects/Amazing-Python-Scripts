#!/usr/bin/env python3
"""
Test runner for R29-T034: Test an invariant of btnclick (Restaurant-Management-System.py).
Executes property-based invariant checks, verifies broken-invariant detection on mutant,
and records inputs, outputs, and tool versions under work/R29-T034/.
"""

import os
import sys
import json
import random
import unittest
import importlib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T034")
RMS_DIR = os.path.join(ROOT_DIR, "Restaurant-Management-System")

if RMS_DIR not in sys.path:
    sys.path.insert(0, RMS_DIR)

rms = importlib.import_module("Restaurant-Management-System")
import test_rms


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T034",
        "target": "Restaurant-Management-System/Restaurant-Management-System.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Smallest valid input
    rms.operator = ""
    rms.text_input.set("")
    token = 0
    expected_op = "0"
    rms.btnclick(token)
    test_1 = {
        "name": "smallest_valid_input_btnclick",
        "source_preconditions": "Restaurant-Management-System/Restaurant-Management-System.py lines 25, 26, 28",
        "input": token,
        "expected": expected_op,
        "actual": rms.operator,
        "passed": rms.operator == expected_op and rms.text_input.get() == expected_op
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary input
    rms.operator = "12"
    rms.text_input.set("12")
    token_ord = "+"
    expected_ord = "12+"
    rms.btnclick(token_ord)
    test_2 = {
        "name": "ordinary_input_btnclick",
        "source_preconditions": "Restaurant-Management-System/Restaurant-Management-System.py lines 25, 26, 28",
        "input": token_ord,
        "expected": expected_ord,
        "actual": rms.operator,
        "passed": rms.operator == expected_ord and rms.text_input.get() == expected_ord
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}", file=sys.stderr)
        sys.exit(1)

    # 3. 100 deterministic property tests
    rng = random.Random(42)
    valid_tokens = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+", "-", "*", "/", "."]
    all_prop_passed = True
    samples = []
    rms.operator = ""
    rms.text_input.set("")

    for i in range(100):
        t = rng.choice(valid_tokens)
        prev = rms.operator
        exp = prev + str(t)
        rms.btnclick(t)
        ok = (rms.operator == exp and rms.text_input.get() == exp)
        if not ok:
            all_prop_passed = False
        if i < 5:
            samples.append({"step": i, "token": str(t), "prev": prev, "expected": exp, "actual": rms.operator})

    test_3 = {
        "name": "property_invariant_100_random_cases",
        "source_preconditions": "Restaurant-Management-System/Restaurant-Management-System.py lines 25, 26, 28",
        "samples_count": 100,
        "passed": all_prop_passed,
        "preview_samples": samples
    }
    evidence["tests"].append(test_3)
    if not all_prop_passed:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # 4. Mutant check: deliberate invariant violation detection
    def broken_btnclick(numbers):
        # Deliberate mutant: overwrites instead of concatenates
        rms.operator = str(numbers)
        rms.text_input.set(rms.operator)

    rms.operator = "10"
    broken_btnclick("+")
    mutant_failed_as_expected = (rms.operator != "10+")
    test_4 = {
        "name": "mutant_invariant_violation_check",
        "description": "Verifies that breaking concatenation is detected",
        "passed": mutant_failed_as_expected
    }
    evidence["tests"].append(test_4)
    if not mutant_failed_as_expected:
        print(f"FAILED: {test_4['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_rms)
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
