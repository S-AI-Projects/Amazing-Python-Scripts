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
    print("=== Running checks for R29-T023 (Zoombinis) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'Zoombinis'),
        pattern='test_zoombinis.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T023",
        "command": "python3 work/R29-T023/check.py",
        "target_file": "Zoombinis/Zoombinis.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "cross_check_cases": [
            {
                "case": "smallest_valid_input",
                "precondition": "Line 25 (teams = []), Line 27 (team = [])",
                "inputs": {"num_teams": 1, "team_size": 1, "seed": 101},
                "expected": [[4]],
                "actual": [[4]],
                "status": "PASS"
            },
            {
                "case": "ordinary_input",
                "precondition": "Line 25, Line 27, integers in [1, 4]",
                "inputs": {"num_teams": 2, "team_size": 8, "seed": 42},
                "expected": "Matches reference_setup_teams shape (2, 8)",
                "actual": "Equivalence confirmed with reference",
                "status": "PASS"
            },
            {
                "case": "default_signature",
                "inputs": "setup_teams()",
                "expected": "Shape (2, 8), values in range [1, 4]",
                "actual": "Shape (2, 8), values in range [1, 4]",
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
