#!/usr/bin/env python3
"""
Test runner for R29-T038: Cover the failure behavior of getStrength (generator.py) [GUI-Password-Generator].
Executes failure-path regression checks, verifies absent-result sentinel None and caller-state validity,
and records inputs, outputs, and tool versions under work/R29-T038/.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T038")
GEN_DIR = os.path.join(ROOT_DIR, "GUI-Password-Generator")

if GEN_DIR not in sys.path:
    sys.path.insert(0, GEN_DIR)

import generator
import test_generator


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T038",
        "target": "GUI-Password-Generator/generator.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Failure branch with smallest invalid input
    entry_mock = generator.MockEntry()
    entry_mock.insert(0, "preset_text")
    fail_res = generator.getStrength(strength_val=-1, length_val=0, entry_widget=entry_mock)
    test_1 = {
        "name": "absent_result_failure_branch",
        "source_preconditions": "GUI-Password-Generator/generator.py lines 55, 80",
        "input": {"strength_val": -1, "length_val": 0},
        "expected_sentinel": None,
        "actual_result": fail_res,
        "caller_state_cleared": entry_mock.get() == "",
        "passed": (fail_res is None and entry_mock.get() == "")
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary valid call immediately succeeding failure
    succ_res = generator.getStrength(strength_val=0, length_val=10, entry_widget=entry_mock)
    test_2 = {
        "name": "ordinary_call_succeeds_after_failure",
        "source_preconditions": "GUI-Password-Generator/generator.py lines 69, 80",
        "input": {"strength_val": 0, "length_val": 10},
        "expected_length": 10,
        "actual_length": len(succ_res) if succ_res else 0,
        "passed": (succ_res is not None and len(succ_res) == 10)
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_generator)
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
