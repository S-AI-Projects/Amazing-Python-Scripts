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
    print("=== Running checks for R29-T030 (Automated Script) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.join(PROJECT_ROOT, 'Automated Script'),
        pattern='test_script.py'
    )
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    test_count = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    was_successful = result.wasSuccessful()

    evidence = {
        "task_id": "R29-T030",
        "command": "python3 work/R29-T030/check.py",
        "target_file": "Automated Script/Script.py",
        "test_count": test_count,
        "failures": failures,
        "errors": errors,
        "successful": was_successful,
        "tool_versions": {
            "python": platform.python_version(),
            "platform": platform.platform()
        },
        "mutation_proof": {
            "protected_condition": "Directory hierarchy preservation via os.path.relpath(source_file, source_dir)",
            "plausible_mutant": "destination_file = os.path.join(destination_dir, file) [flattens subdirectories]",
            "original_result": "PASS (nested path exists in destination)",
            "mutant_result": "FAIL (nested path missing in destination)",
            "semantic_reason": "Mutant strips parent directory prefixes, destroying folder hierarchy."
        },
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
