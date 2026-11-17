#!/usr/bin/env python3
"""
Test runner for R29-T031: Lock down the contract of Songs By Artist (config.py).
Executes focused regression checks and records inputs, expected vs actual outputs,
and tool versions under work/R29-T031/.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T031")
SONGS_BY_ARTIST_DIR = os.path.join(ROOT_DIR, "Songs-By-Artist")

if SONGS_BY_ARTIST_DIR not in sys.path:
    sys.path.insert(0, SONGS_BY_ARTIST_DIR)

import config
import test_config


def run_checks():
    evidence = {
        "task": "R29-T031",
        "target": "Songs-By-Artist/config.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Default config check (smallest input)
    expected_default = {"client_id": "", "secret_key": ""}
    actual_default = config.get_config()
    test_1 = {
        "name": "smallest_input_default_config",
        "source_preconditions": "Songs-By-Artist/config.py lines 12-13, 16",
        "input": None,
        "expected": expected_default,
        "actual": actual_default,
        "passed": actual_default == expected_default
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}: expected {expected_default}, got {actual_default}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary input check
    ordinary_input = {
        "client_id": "1234567890abcdef1234567890abcdef",
        "secret_key": "abcdef1234567890abcdef1234567890"
    }
    actual_ordinary = config.validate_config(ordinary_input["client_id"], ordinary_input["secret_key"])
    expected_ordinary = True
    test_2 = {
        "name": "ordinary_credentials_input",
        "source_preconditions": "Songs-By-Artist/config.py line 21",
        "input": ordinary_input,
        "expected": expected_ordinary,
        "actual": actual_ordinary,
        "passed": actual_ordinary == expected_ordinary
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}: expected {expected_ordinary}, got {actual_ordinary}", file=sys.stderr)
        sys.exit(1)

    # 3. Repeated-value boundary check
    repeated_input = {
        "client_id": "a" * 32,
        "secret_key": "b" * 32
    }
    actual_repeated = config.validate_config(repeated_input["client_id"], repeated_input["secret_key"])
    expected_repeated = True
    test_3 = {
        "name": "repeated_value_boundary_input",
        "source_preconditions": "Songs-By-Artist/config.py line 21",
        "input": repeated_input,
        "expected": expected_repeated,
        "actual": actual_repeated,
        "passed": actual_repeated == expected_repeated
    }
    evidence["tests"].append(test_3)
    if not test_3["passed"]:
        print(f"FAILED: {test_3['name']}: expected {expected_repeated}, got {actual_repeated}", file=sys.stderr)
        sys.exit(1)

    # Run native unittest suite
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_config)
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
