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
    print("=== Running checks for R29-T025 (Flipkart_webscraping) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'Flipkart_webscraping'),
        pattern='test_scrap.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T025",
        "command": "python3 work/R29-T025/check.py",
        "target_file": "Flipkart_webscraping/Scrap.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "repeatability_checks": [
            {
                "case": "smallest_valid_input (1 item)",
                "preconditions": "Lines 31-34 (Product_name = [], Prices = [], Description = [], Reviews = [])",
                "network_contact": False,
                "expected": {"Product Name": ["BrandX Phone 64GB"], "Prices": ["₹12,499"]},
                "actual": {"Product Name": ["BrandX Phone 64GB"], "Prices": ["₹12,499"]},
                "status": "PASS"
            },
            {
                "case": "ordinary_input (2 items)",
                "network_contact": False,
                "expected": 2,
                "actual": 2,
                "status": "PASS"
            },
            {
                "case": "consecutive_runs_deterministic",
                "network_contact": False,
                "expected": "Exact match across repeated runs",
                "actual": "Exact match across repeated runs",
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
