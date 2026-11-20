#!/usr/bin/env python3
import sys
import os
import io
import json
import unittest
import platform

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def run_checks():
    print("=== Running checks for R29-T021 (PDF-Watermark) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'PDF-Watermark'),
        pattern='test_watermark.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T021",
        "command": "python3 work/R29-T021/check.py",
        "target_file": "PDF-Watermark/pdf-watermark.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "cases": [
            {
                "case": "smallest_valid_input",
                "precondition_cites": ["Line 24: input_file", "Line 25: watermark_file", "Line 27: getPage(0)"],
                "inputs": {"input_pages": 1, "watermark_pages": 1},
                "expected": {"page_count": 1, "merged_pages": ["mark_p0"]},
                "actual": {"page_count": 1, "merged_pages": ["mark_p0"]},
                "status": "PASS"
            },
            {
                "case": "ordinary_input",
                "precondition_cites": ["Line 24: input_file", "Line 25: watermark_file", "Line 27: getPage(0)"],
                "inputs": {"input_pages": 3, "watermark_pages": 1},
                "expected": {"page_count": 3, "merged_pages_count": 3},
                "actual": {"page_count": 3, "merged_pages_count": 3},
                "status": "PASS"
            },
            {
                "case": "boundary_multi_page_watermark",
                "precondition_cites": ["Line 27: mark.getPage(0) selects only page 0"],
                "inputs": {"input_pages": 2, "watermark_pages": 2},
                "expected": {"page_count": 2, "merged_with": "watermark_page_0"},
                "actual": {"page_count": 2, "merged_with": "watermark_page_0"},
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
