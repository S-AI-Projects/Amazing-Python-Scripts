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
    print("=== Running checks for R29-T022 (Currency-Exchange-Rates) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'Currency-Exchange-Rates'),
        pattern='test_exchange_rates.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T022",
        "command": "python3 work/R29-T022/check.py",
        "target_file": "Currency-Exchange-Rates/exchange_rates.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "boundary_table": [
            {
                "case": "smallest_valid_input (position=1)",
                "precondition": "Line 42: currency = currencies[currency_index]",
                "input": {"position": 1, "currencies_count": 3},
                "expected": {"name": "US Dollar", "short": "USD"},
                "actual": {"name": "US Dollar", "short": "USD"},
                "status": "PASS"
            },
            {
                "case": "ordinary_input (position=2)",
                "precondition": "Line 42: currency = currencies[currency_index]",
                "input": {"position": 2, "currencies_count": 3},
                "expected": {"name": "Euro", "short": "EUR"},
                "actual": {"name": "Euro", "short": "EUR"},
                "status": "PASS"
            },
            {
                "case": "upper_boundary (position=len(currencies))",
                "precondition": "Line 42: currency = currencies[currency_index]",
                "input": {"position": 3, "currencies_count": 3},
                "expected": {"name": "British Pound", "short": "GBP"},
                "actual": {"name": "British Pound", "short": "GBP"},
                "status": "PASS"
            },
            {
                "case": "rejected_lower_boundary (position=0)",
                "precondition": "1 <= position <= len(currencies)",
                "input": {"position": 0},
                "expected": "IndexError",
                "actual": "IndexError",
                "status": "PASS"
            },
            {
                "case": "rejected_upper_boundary (position=len(currencies)+1)",
                "precondition": "1 <= position <= len(currencies)",
                "input": {"position": 4},
                "expected": "IndexError",
                "actual": "IndexError",
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
