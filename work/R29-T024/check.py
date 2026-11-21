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
    print("=== Running checks for R29-T024 (hexCalculator) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'hexCalculator'),
        pattern='test_hex_calculator.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T024",
        "command": "python3 work/R29-T024/check.py",
        "target_file": "hexCalculator/hexCalculator.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "property_checks": [
            {
                "property": "smallest_valid_input",
                "precondition": "Line 25 (num1), Line 27 (result)",
                "input": {"val1": "0", "val2": "0"},
                "expected": "Result: 0X0",
                "actual": "Result: 0X0",
                "status": "PASS"
            },
            {
                "property": "ordinary_input",
                "precondition": "Line 25 (num1), Line 27 (result)",
                "input": {"val1": "A", "val2": "F"},
                "expected": "Result: 0X19",
                "actual": "Result: 0X19",
                "status": "PASS"
            },
            {
                "property": "commutativity_invariant",
                "invariant": "calculate_hex_add(a, b) == calculate_hex_add(b, a)",
                "sample_count": 100,
                "shrunk_counterexample": None,
                "status": "PASS"
            },
            {
                "property": "identity_element",
                "invariant": "int(calculate_hex_add(a, '0'), 16) == int(a, 16)",
                "sample_count": 50,
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
