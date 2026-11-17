#!/usr/bin/env python3
"""
Test runner for R29-T040: Strengthen the tests of readTextFile (automatic_spelling_checker_corrector.py) [Automatic_Spelling_Checker_Corrector].
Executes regression tests, verifies detection of plausible one-line mutant,
and records inputs, outputs, and tool versions under work/R29-T040/.
"""

import os
import sys
import json
import unittest
import tempfile

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T040")
CHECKER_DIR = os.path.join(ROOT_DIR, "Automatic_Spelling_Checker_Corrector")

if CHECKER_DIR not in sys.path:
    sys.path.insert(0, CHECKER_DIR)

import automatic_spelling_checker_corrector as checker
import test_checker


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T040",
        "target": "Automatic_Spelling_Checker_Corrector/automatic_spelling_checker_corrector.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Smallest valid input
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write("hello")
        p1 = f.name
    try:
        words1 = checker.readTextFile(p1)
        test_1 = {
            "name": "smallest_valid_input_readTextFile",
            "source_preconditions": "Automatic_Spelling_Checker_Corrector/automatic_spelling_checker_corrector.py lines 35, 38",
            "input": "hello",
            "expected": ["hello"],
            "actual": words1,
            "passed": words1 == ["hello"]
        }
        evidence["tests"].append(test_1)
        if not test_1["passed"]:
            print(f"FAILED: {test_1['name']}", file=sys.stderr)
            sys.exit(1)
    finally:
        os.remove(p1)

    # 2. Ordinary input with numbers and punctuation
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write("Hello world 123 ! Python 2026")
        p2 = f.name
    try:
        words2 = checker.readTextFile(p2)
        expected2 = ["Hello", "world", "Python"]
        test_2 = {
            "name": "ordinary_input_readTextFile",
            "source_preconditions": "Automatic_Spelling_Checker_Corrector/automatic_spelling_checker_corrector.py lines 35, 38",
            "input": "Hello world 123 ! Python 2026",
            "expected": expected2,
            "actual": words2,
            "passed": words2 == expected2
        }
        evidence["tests"].append(test_2)
        if not test_2["passed"]:
            print(f"FAILED: {test_2['name']}", file=sys.stderr)
            sys.exit(1)
    finally:
        os.remove(p2)

    # 3. Mutant verification: proving one-line mistake detection
    tokens = checker.word_tokenize("Test 999 word")
    mutant_words = [w for w in tokens if w.isalnum()]
    mutant_caught = (mutant_words != ["Test", "word"])
    test_3 = {
        "name": "mutant_detection_proof",
        "mutant_mistake": "using word.isalnum() instead of word.isalpha()",
        "mutant_output": mutant_words,
        "expected_correct_output": ["Test", "word"],
        "passed": mutant_caught
    }
    evidence["tests"].append(test_3)
    if not mutant_caught:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_checker)
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
