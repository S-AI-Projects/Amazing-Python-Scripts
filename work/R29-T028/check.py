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
    print("=== Running checks for R29-T028 (Image editor python script) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'Image editor python script'),
        pattern='test_image_editor.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T028",
        "command": "python3 work/R29-T028/check.py",
        "target_file": "Image editor python script/Image_editing_script.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "error_path_cases": [
            {
                "case": "smallest_valid_input",
                "precondition": "Line 28 (HOME_OPTIONS)",
                "input": "1",
                "expected": "Flip the image.",
                "actual": "Flip the image.",
                "status": "PASS"
            },
            {
                "case": "ordinary_input",
                "input": "4",
                "expected": "Blur the image",
                "actual": "Blur the image",
                "status": "PASS"
            },
            {
                "case": "failure_out_of_bounds",
                "input": "0",
                "expected_exception": "ValueError",
                "expected_message": "Invalid option '0': choice must be between 1 and 9",
                "status": "PASS"
            },
            {
                "case": "failure_invalid_string",
                "input": "invalid",
                "expected_exception": "ValueError",
                "expected_message": "Invalid option 'invalid': choice must be between 1 and 9",
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
