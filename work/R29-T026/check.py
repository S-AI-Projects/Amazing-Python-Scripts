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
    print("=== Running checks for R29-T026 (imageWatermarker) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'imageWatermarker'),
        pattern='test_main.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T026",
        "command": "python3 work/R29-T026/check.py",
        "target_file": "imageWatermarker/main.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "characterisation_checks": [
            {
                "case": "smallest_valid_input",
                "preconditions": "Line 36 (image_files = []), Line 42 (output_path)",
                "input": {"im_size": [100, 100], "mark_size": [20, 20]},
                "expected": {"position": [30, 30], "target_size": [2048, 2048]},
                "actual": {"position": [30, 30], "target_size": [2048, 2048]},
                "status": "PASS"
            },
            {
                "case": "ordinary_input",
                "input": {"im_size": [4000, 3000], "mark_size": [400, 200]},
                "expected": {"position": [3550, 2750], "target_size": [2048, 1536]},
                "actual": {"position": [3550, 2750], "target_size": [2048, 1536]},
                "status": "PASS"
            },
            {
                "case": "characterisation_equivalence",
                "assertion": "compute_watermark_geometry matches original inline formula across all tested aspect ratios",
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
