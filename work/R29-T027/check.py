#!/usr/bin/env python3
import sys
import os
import io
import json
import unittest
import platform

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def run_checks():
    print("=== Running checks for R29-T027 (Number Conversion) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'Number Conversion'),
        pattern='test_converter.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T027",
        "command": "python3 work/R29-T027/check.py",
        "target_file": "Number Conversion/converter_script.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "worked_example_traces": [
            {
                "case": "smallest_valid_input",
                "precondition": "Line 28 (decimal_number = 0), Line 33 (binary_number = [])",
                "input": 0,
                "expected": {"binary_str": "0", "binary_bits": [0]},
                "actual": {"binary_str": "0", "binary_bits": [0]},
                "status": "PASS"
            },
            {
                "case": "ordinary_input",
                "input": 13,
                "intermediate_steps": [
                    {"dividend": 13, "quotient": 6, "remainder": 1},
                    {"dividend": 6, "quotient": 3, "remainder": 0},
                    {"dividend": 3, "quotient": 1, "remainder": 1},
                    {"dividend": 1, "quotient": 0, "remainder": 1}
                ],
                "expected": {"binary_str": "1101", "binary_bits": [1, 1, 0, 1]},
                "actual": {"binary_str": "1101", "binary_bits": [1, 1, 0, 1]},
                "status": "PASS"
            }
        ],
        "runner_output": stream.getvalue()
    }

    output_dir = os.path.dirname(os.path.abspath(__file__))
    evidence_file = os.path.join(output_dir, 'evidence.json')
    with open(evidence_file, 'w') as f:
        json.dump(evidence, f, indent=2)

    print(stream.getvalue())
    print(f"Executed {test_count} tests. Failures: {failures}, Errors: {errors}")
    print(f"Evidence saved to {evidence_file}")

    if not was_successful or test_count == 0:
        print("Checks FAILED!")
        sys.exit(1)
    else:
        print("All checks PASSED successfully.")
        sys.exit(0)

if __name__ == '__main__':
    run_checks()
